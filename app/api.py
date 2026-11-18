"""Minimal research-only HTTP API for raw dense retrieval.

The default embedder is strictly cache-only. It never calls Cohere; cache misses
fail closed until an authorized local or external query encoder is configured.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr

from app import config
from app.answer.answer_generator import (
    GREETING_REPLY,
    OUT_OF_SCOPE_REPLY,
    SAFETY_NOTICE,
    dosing_refusal,
    is_dosing_question,
)
from app.answer.answer_generator import generate as generate_answer
from app.retrieval.citation_validation import validate as validate_citations
from app.retrieval.dense import DenseRetriever
from app.retrieval.embeddings import EmbeddingProfile
from app.retrieval.evidence_gate import assess as assess_evidence
from app.retrieval.query_embedding import CachedQueryEmbedder
from app.retrieval.research_reader import ResearchVectorReader
from app.retrieval.types import RetrievalError, RetrievalProfile
from app.router.classifier import classify as classify_intent

FRONTEND_DIR = config.ROOT / "frontend"


class RetrieveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: StrictStr
    top_k: StrictInt = 10


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    query: StrictStr
    top_k: StrictInt = 5


# category -> (http_status, user-facing error code, Vietnamese explanation; never provider/DB internals)
CHAT_ERRORS: dict[str, tuple[int, str, str]] = {
    "invalid_query": (422, "INVALID_QUERY", "Câu hỏi trống hoặc vượt quá độ dài cho phép."),
    "invalid_k": (422, "INVALID_TOP_K", "Số lượng kết quả yêu cầu (top_k) nằm ngoài phạm vi cho phép."),
    "embedding_unavailable": (503, "QUERY_NOT_CACHED",
        "Câu hỏi này chưa có vector truy vấn trong cache cục bộ (CACHE-ONLY). Gửi câu hỏi trực tiếp tới "
        "Cohere hiện CHƯA được chủ dự án cho phép (xem T2.6: APPROVAL_REQUIRED). Vui lòng thử một câu hỏi "
        "mẫu, hoặc chờ phê duyệt trước khi dùng câu hỏi tự do."),
    "embedding_failed": (503, "EMBEDDING_FAILED", "Không thể xác thực vector truy vấn một cách an toàn."),
    "database_unavailable": (503, "DB_UNAVAILABLE", "Không thể kết nối cơ sở dữ liệu truy xuất nghiên cứu."),
    "permission_denied": (503, "PERMISSION_DENIED", "Vai trò đọc nghiên cứu không có quyền truy cập view đã ủy quyền."),
    "view_missing": (503, "VIEW_MISSING", "View truy xuất đã ủy quyền hiện không khả dụng."),
    "wrong_role": (503, "WRONG_ROLE", "Kiểm tra vai trò kết nối cơ sở dữ liệu thất bại."),
    "query_timeout": (503, "QUERY_TIMEOUT", "Truy vấn truy xuất vượt quá thời gian cho phép."),
    "configuration_error": (503, "CONFIG_ERROR", "Hệ thống truy xuất chưa được cấu hình an toàn."),
    "cache_invalid": (503, "CACHE_INVALID", "Vector truy vấn trong cache không hợp lệ."),
    "provenance_invalid": (502, "PROVENANCE_INVALID", "Kết quả truy xuất không vượt qua kiểm tra nguồn gốc."),
}


def _chat_evidence(details) -> list[dict]:
    """Verified metadata only, taken from the already-validated RetrievedChunk rows. Nothing invented.

    `support_type` ("direct"/"indirect"/"generic") is the Evidence Gate's own classification of how
    strongly this chunk backs the question — surfaced to the caller rather than collapsed into a single
    pass/fail bit. See `app/retrieval/evidence_gate.py`.
    """
    items = []
    for d in details:
        chunk = d.chunk
        items.append({
            "citation_id": f"C{chunk.rank}",
            "source_id": chunk.source_id,
            "title": chunk.title or None,
            "section": chunk.section or None,
            "page": chunk.page,
            "char_range": chunk.char_range,
            "source_url": chunk.source_url or None,
            "excerpt": chunk.content,
            "rank": chunk.rank,
            "support_type": d.support_type,
            "age_mismatch": d.age_mismatch,
        })
    return items


def _chat_citations(evidence: list[dict]) -> list[dict]:
    return [{"citation_id": e["citation_id"], "source_id": e["source_id"], "title": e["title"],
              "source_url": e["source_url"], "locator": e["page"] or e["char_range"]} for e in evidence]


def _blocked_chat_response(category: str) -> JSONResponse:
    status_code, code, message = CHAT_ERRORS.get(category, (500, "INTERNAL_ERROR", "Truy xuất thất bại an toàn."))
    retrieval_status = "blocked_uncached" if category == "embedding_unavailable" else "error"
    return JSONResponse(status_code=status_code, content={
        "status": "blocked" if category == "embedding_unavailable" else "error",
        "answer": None,
        "answer_mode": "none",
        "retrieval_status": retrieval_status,
        "evidence": [],
        "citations": [],
        "warnings": [SAFETY_NOTICE],
        "error": {"code": code, "message": message},
    })


def build_offline_retriever() -> DenseRetriever:
    """Build the baseline with no external embedding fallback."""
    retrieval_profile = RetrievalProfile.load("dense_baseline_v1")
    embedding_profile = EmbeddingProfile.load(retrieval_profile.embedding_profile)
    embedder = CachedQueryEmbedder(embedding_profile, retrieval_profile.query_cache_dir, inner=None)
    reader = ResearchVectorReader(retrieval_profile)
    return DenseRetriever(retrieval_profile, embedder, reader)


def _error_status(category: str) -> int:
    if category in {"invalid_query", "invalid_k"}:
        return 422
    if category in {"embedding_unavailable", "embedding_failed", "database_unavailable", "permission_denied",
                    "view_missing", "wrong_role", "query_timeout", "configuration_error", "cache_invalid"}:
        return 503
    return 502


def create_app(retriever: DenseRetriever | None = None) -> FastAPI:
    active_retriever = retriever or build_offline_retriever()
    app = FastAPI(title="ASD-RAG Dense Retrieval", version="0.1.0", docs_url=None, redoc_url=None)
    app.state.dense_retriever = active_retriever

    @app.post("/api/retrieve")
    def retrieve(request: RetrieveRequest) -> dict:
        try:
            response = active_retriever.retrieve(request.query, k=request.top_k)
        except RetrievalError as exc:
            safe_messages = {
                "invalid_query": "Query is empty or exceeds the allowed length.",
                "invalid_k": "top_k is outside the configured range.",
                "embedding_unavailable": "No authorized query embedding is available for this query.",
                "embedding_failed": "Query embedding failed.",
                "database_unavailable": "Research retrieval database is unavailable.",
                "permission_denied": "Research reader cannot access the authorized view.",
                "view_missing": "Authorized research retrieval view is unavailable.",
                "wrong_role": "Research reader authorization check failed.",
                "query_timeout": "Research retrieval exceeded its time limit.",
                "configuration_error": "Dense retrieval is not configured safely.",
                "cache_invalid": "Cached query vector failed validation.",
                "provenance_invalid": "Retrieved result provenance failed validation.",
            }
            raise HTTPException(status_code=_error_status(exc.category), detail={
                "code": exc.category, "message": safe_messages.get(exc.category, "Retrieval failed safely.")}) from None
        except Exception:
            # Never return driver/provider exception text or credentials to the caller.
            raise HTTPException(status_code=500, detail={
                "code": "internal_error", "message": "Retrieval failed safely."}) from None

        embedding_model = (response.results[0].model_id if response.results
                           else EmbeddingProfile.load(response.embedding_profile).model_id)
        return {
            "query": request.query,
            "retrieval_method": response.retriever,
            "embedding_model": embedding_model,
            "top_k": response.k_requested,
            "result_count": len(response.results),
            "results": [{
                "rank": item.rank,
                "chunk_id": item.chunk_id,
                "source_id": item.source_id,
                "document_title": item.title,
                "section": item.section,
                "page": item.page,
                "content": item.content,
                "similarity": item.cosine_similarity,
            } for item in response.results],
            "status": "success" if response.status == "ok" else "no_results",
        }

    @app.post("/api/chat")
    def chat(request: ChatRequest) -> JSONResponse:
        """Cache-only demo chat: intent routing -> retrieval -> Evidence Sufficiency Gate ->
        Citation Validation -> non-LLM answer generation (template / extractive fallback / refusal).

        Never calls Cohere, a reranker, or an external LLM (config.ENABLE_LIVE_* are fixed False/fail-closed).
        An uncached ASD question returns HTTP 503 QUERY_NOT_CACHED rather than a synthetic/incompatible vector.
        A greeting or an out-of-scope message never reaches the embedder or the database at all.
        """
        try:
            text = active_retriever.validate_query(request.query)
            k_ok = active_retriever.validate_k(request.top_k)
        except RetrievalError as exc:
            return _blocked_chat_response(exc.category)

        intent = classify_intent(text)

        if intent.branch == "greeting":
            return JSONResponse(status_code=200, content={
                "status": "ok", "answer": GREETING_REPLY[intent.greeting_kind or "greeting"],
                "answer_mode": "greeting_template", "retrieval_status": "skipped_greeting",
                "evidence": [], "citations": [], "warnings": [], "error": None,
            })
        if intent.branch == "out_of_scope":
            return JSONResponse(status_code=200, content={
                "status": "ok", "answer": OUT_OF_SCOPE_REPLY, "answer_mode": "out_of_scope",
                "retrieval_status": "out_of_scope", "evidence": [], "citations": [],
                "warnings": [SAFETY_NOTICE], "error": None,
            })

        if is_dosing_question(text):
            # Refused before any embedding/database call — a dangerous medication-dosing question must
            # never surface a generic "not cached" error instead of a safe refusal (found live during
            # this task's eval/datasets/asd_qa_eval_v2.jsonl run: qe069/qe071).
            d = dosing_refusal()
            return JSONResponse(status_code=200, content={
                "status": "ok", "answer": d.text, "answer_mode": d.mode,
                "retrieval_status": "refused_before_retrieval", "evidence": [], "citations": [],
                "warnings": [SAFETY_NOTICE], "error": None,
            })

        try:
            response = active_retriever.retrieve(text, k=k_ok)
        except RetrievalError as exc:
            return _blocked_chat_response(exc.category)
        except Exception:
            return _blocked_chat_response("internal_error")

        gate = assess_evidence(text, response.results)
        evidence = validate_citations(_chat_evidence(gate.details), gate.supported)
        answer = generate_answer(text, evidence)
        # Only the evidence the answer actually cites is shown — e.g. a topic template may be grounded
        # in 1 of 4 supporting chunks; the rest stay out of the user-facing response.
        cited = set(answer.citation_ids)
        evidence = [e for e in evidence if e["citation_id"] in cited]

        retrieval_status = response.status if gate.sufficient else "insufficient_evidence"
        warnings = [SAFETY_NOTICE]
        if not gate.sufficient:
            warnings.append("Bằng chứng truy xuất được không đủ liên quan/cụ thể để trả lời chắc chắn câu hỏi này.")
        if intent.confidence == "low":
            warnings.append("Hệ thống không hoàn toàn chắc chắn câu hỏi này thuộc phạm vi ASD; "
                            "kết quả dưới đây dựa trên bằng chứng thực tế tìm được, không suy diễn thêm.")
        if evidence and all(e["support_type"] != "direct" for e in evidence):
            warnings.append("Giới hạn: bằng chứng chỉ đề cập chủ đề này gián tiếp, không phải nguồn "
                            "chuyên biệt về chủ đề — câu trả lời có thể chưa đầy đủ.")
        if any(e.get("age_mismatch") for e in evidence):
            warnings.append("Giới hạn: bằng chứng không xác nhận rõ độ tuổi cụ thể được hỏi.")
        return JSONResponse(status_code=200, content={
            "status": "ok",
            "answer": answer.text,
            "answer_mode": answer.mode,
            "retrieval_status": retrieval_status,
            "evidence": evidence,
            "citations": _chat_citations(evidence),
            "warnings": warnings,
            "error": None,
        })

    @app.get("/api/system/status")
    def system_status() -> dict:
        """Lets the frontend show live DEMO MODE / disabled-provider state instead of hardcoding it."""
        return {
            "demo_mode": config.DEMO_MODE,
            "live_query_embedding_enabled": config.ENABLE_LIVE_QUERY_EMBEDDING,
            "live_reranking_enabled": config.ENABLE_LIVE_RERANKING,
            "live_llm_enabled": config.ENABLE_LIVE_LLM,
            "retrieval_profile": active_retriever.profile.code,
            "safety_notice": SAFETY_NOTICE,
        }

    if FRONTEND_DIR.is_dir():
        app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

    return app


app = create_app()
