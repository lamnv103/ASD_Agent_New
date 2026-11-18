"""Dense retrieval baseline (Phase 6.2 T2.3.1): query -> query embedding -> authorized view -> top-k.

No query expansion, no reranking, no evidence gate, no answer generation. Every failure raises a
RetrievalError (fail closed); a partially valid result set is never returned.
"""

from __future__ import annotations

import hashlib
import math
import time
import uuid
from collections.abc import Callable, Sequence
from datetime import UTC, datetime

from app.retrieval.audit_log import JsonlRetrievalLog
from app.retrieval.query_embedding import QueryEmbedder, check_vector
from app.retrieval.research_reader import ResearchVectorReader
from app.retrieval.types import RetrievalError, RetrievalProfile, RetrievalResponse, RetrievedChunk


def query_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def format_page(start: int | None, end: int | None) -> str | None:
    if start is None:
        return None
    return str(start) if end in (None, start) else f"{start}-{end}"


class DenseRetriever:
    def __init__(self, profile: RetrievalProfile, embedder: QueryEmbedder, reader: ResearchVectorReader,
                 log: JsonlRetrievalLog | None = None, clock: Callable[[], float] = time.perf_counter) -> None:
        if embedder.profile.profile_code != profile.embedding_profile:
            raise RetrievalError("profile_mismatch", "query embedder profile differs from the retrieval profile")
        if embedder.profile.similarity_metric != profile.similarity_metric:
            raise RetrievalError("profile_mismatch", "embedding metric differs from the retrieval metric")
        self.profile = profile
        self.embedder = embedder
        self.reader = reader
        self.log = log
        self._clock = clock

    # ------------------------------------------------------------------------------------------ public
    def validate_query(self, query: object) -> str:
        if not isinstance(query, str) or not query.strip():
            raise RetrievalError("invalid_query", "query is empty")
        text = query.strip()
        if len(text) > self.profile.max_query_chars:
            raise RetrievalError("invalid_query", f"query longer than {self.profile.max_query_chars} characters")
        return text

    def validate_k(self, k: object) -> int:
        k = self.profile.k_default if k is None else k
        if isinstance(k, bool) or not isinstance(k, int) or not 1 <= k <= self.profile.k_max:
            raise RetrievalError("invalid_k", f"k must be an integer in [1, {self.profile.k_max}]")
        return k

    def retrieve(self, query: str, k: int | None = None, question_id: str | None = None) -> RetrievalResponse:
        start = self._clock()
        request_id = str(uuid.uuid4())
        text, k_ok, qhash = None, None, None
        try:
            text = self.validate_query(query)
            k_ok = self.validate_k(k)
            qhash = query_sha256(text)
            t0 = self._clock()
            vectors = self.embedder.embed_queries([text])
            if not isinstance(vectors, list) or len(vectors) != 1:
                raise RetrievalError("embedding_failed", "query embedder returned an invalid vector count")
            vector = check_vector(vectors[0], self.embedder.profile)
            embed_ms = (self._clock() - t0) * 1000
            response = self._search(vector, k_ok, request_id, question_id, qhash)
            response.latency_ms.update(embed=round(embed_ms, 2), total=round((self._clock() - start) * 1000, 2))
        except RetrievalError as exc:
            self._log_error(request_id, question_id, qhash, k_ok, exc, start)
            raise
        self._log_ok(response)
        return response

    def retrieve_by_vector(self, vector: Sequence[float], k: int | None = None, question_id: str | None = None,
                           query_hash: str = "vector-fixture") -> RetrievalResponse:
        """Database half of the pipeline with a given vector (tests, cached evaluation). Same checks."""
        start = self._clock()
        request_id = str(uuid.uuid4())
        k_ok = None
        try:
            k_ok = self.validate_k(k)
            vec = check_vector(list(vector), self.embedder.profile)
            response = self._search(vec, k_ok, request_id, question_id, query_hash)
            response.latency_ms["total"] = round((self._clock() - start) * 1000, 2)
        except RetrievalError as exc:
            self._log_error(request_id, question_id, query_hash, k_ok, exc, start)
            raise
        self._log_ok(response)
        return response

    # ----------------------------------------------------------------------------------------- private
    def _search(self, vector: list[float], k: int, request_id: str, question_id: str | None,
                qhash: str) -> RetrievalResponse:
        t0 = self._clock()
        rows = self.reader.search(vector, k)
        db_ms = (self._clock() - t0) * 1000
        chunk_ids = [row.get("chunk_id") for row in rows]
        if any(not isinstance(chunk_id, str) or not chunk_id for chunk_id in chunk_ids):
            raise RetrievalError("provenance_invalid", "database returned a missing or invalid chunk ID")
        if len(chunk_ids) != len(set(chunk_ids)):
            raise RetrievalError("provenance_invalid", "database returned duplicate chunk IDs")
        results = [self._to_chunk(row, rank) for rank, row in enumerate(rows, 1)]
        auth = {r.authorization_version for r in results}
        if len(auth) > 1:
            raise RetrievalError("provenance_invalid", "results come from more than one authorization")
        if len(results) > k:
            raise RetrievalError("provenance_invalid", "database returned more rows than k")
        return RetrievalResponse(
            request_id=request_id, question_id=question_id, retriever=self.profile.code,
            status="ok" if results else "no_results", k_requested=k, query_sha256=qhash,
            query_expansion=False, embedding_profile=self.profile.embedding_profile,
            authorization_version=next(iter(auth)) if auth else None, results=results,
            latency_ms={"db": round(db_ms, 2)}, timestamp=datetime.now(UTC).isoformat(timespec="milliseconds"))

    def _to_chunk(self, row: dict, rank: int) -> RetrievedChunk:
        ep = self.embedder.profile
        problems = []
        for key in ("chunk_id", "source_id", "document_id", "content", "content_sha256", "chunking_profile",
                    "document_version", "authorization_id"):
            if row.get(key) in (None, ""):
                problems.append(f"missing {key}")
        if row.get("page_start") is None and (row.get("char_start") is None or row.get("char_end") is None):
            problems.append("no page and no character range")
        content = row.get("content")
        if content and hashlib.sha256(content.encode("utf-8")).hexdigest() != row.get("content_sha256"):
            problems.append("content hash mismatch")
        if (row.get("profile_code"), row.get("model_id"), row.get("vector_dimension")) != (
                ep.profile_code, ep.model_id, ep.vector_dimension):
            problems.append("embedding profile/model/dimension mismatch")
        distance = row.get("distance")
        if not isinstance(distance, int | float) or not math.isfinite(distance) or not -1e-6 <= distance <= 2 + 1e-6:
            problems.append("distance outside the cosine-distance range")
        if problems:
            raise RetrievalError("provenance_invalid", f"rank {rank}: " + "; ".join(problems))
        section = row.get("section_heading") or " > ".join(row.get("section_path") or [])
        char_range = None if row.get("char_start") is None else f"{row['char_start']}-{row['char_end']}"
        return RetrievedChunk(
            rank=rank, chunk_id=row["chunk_id"], source_id=row["source_id"], document_id=row["document_id"],
            title=row.get("title") or "", source_url=row.get("source_url") or "", content=row["content"],
            content_sha256=row["content_sha256"], section=section,
            page=format_page(row.get("page_start"), row.get("page_end")), char_range=char_range,
            score_type=self.profile.score_type, score=float(distance), cosine_similarity=1.0 - float(distance),
            authorization_version=int(row["authorization_id"]), embedding_profile=row["profile_code"],
            model_id=row["model_id"], corpus_version=f"{row['chunking_profile']}@{row['document_version']}")

    def _log_ok(self, r: RetrievalResponse) -> None:
        if self.log:
            self.log.write({
                "event": "retrieval", "status": r.status, "request_id": r.request_id, "question_id": r.question_id,
                "retriever": r.retriever, "embedding_profile": r.embedding_profile, "query_sha256": r.query_sha256,
                "query_expansion": False, "authorization_version": r.authorization_version, "k": r.k_requested,
                "returned": [{"rank": c.rank, "chunk_id": c.chunk_id, "cosine_distance": round(c.score, 6)}
                             for c in r.results],
                "latency_ms": r.latency_ms, "timestamp": r.timestamp})

    def _log_error(self, request_id: str, question_id: str | None, qhash: str | None, k: int | None,
                   exc: RetrievalError, start: float) -> None:
        if self.log:
            self.log.write({
                "event": "retrieval", "status": "error", "error_category": exc.category, "request_id": request_id,
                "question_id": question_id, "retriever": self.profile.code,
                "embedding_profile": self.profile.embedding_profile, "query_sha256": qhash,
                "query_expansion": False, "k": k, "returned": [],
                "latency_ms": {"total": round((self._clock() - start) * 1000, 2)},
                "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds")})
