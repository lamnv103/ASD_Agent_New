"""Cohere client and pipeline helpers, with a mocked transport: no network, no real key."""

import json
from dataclasses import replace

import httpx
import pytest

from app.ingest.embed_pipeline import build_input, input_hash, l2_norm
from app.retrieval.embeddings import CohereEmbedder, EmbeddingError, EmbeddingProfile, validate_vector

PROFILE = EmbeddingProfile.load("cohere_embed_v4_1536_v1")
SMALL = replace(PROFILE, vector_dimension=4, base_delay_seconds=0.0)
FAKE_KEY = "test-key-not-real"


def vector(n: int = 4) -> list[float]:
    return [0.5] * n


def mock(handler) -> CohereEmbedder:
    return CohereEmbedder(SMALL, FAKE_KEY, transport=httpx.MockTransport(handler), sleep=lambda s: None)


def test_profile_matches_the_verified_configuration():
    assert (PROFILE.model_id, PROFILE.vector_dimension) == ("embed-v4.0", 1536)
    assert (PROFILE.document_input_type, PROFILE.query_input_type) == ("search_document", "search_query")
    assert PROFILE.max_texts_per_call == 96 and PROFILE.truncate == "NONE"


def test_batches_of_96_and_exact_payload():
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        seen.append(body)
        assert request.headers["Authorization"] == f"Bearer {FAKE_KEY}"
        return httpx.Response(200, json={"embeddings": {"float": [vector() for _ in body["texts"]]}})

    out = mock(handler).embed([f"t{i}" for i in range(100)], "search_document")
    assert len(out) == 100 and [len(b["texts"]) for b in seen] == [96, 4]
    assert seen[0] | {"texts": []} == {"model": "embed-v4.0", "texts": [], "input_type": "search_document",
                                       "embedding_types": ["float"], "output_dimension": 4, "truncate": "NONE"}


def test_retries_rate_limit_then_succeeds():
    responses = iter([httpx.Response(429), httpx.Response(503),
                      httpx.Response(200, json={"embeddings": {"float": [vector()]}})])
    embedder = mock(lambda request: next(responses))
    assert embedder.embed(["x"], "search_query") == [vector()] and embedder.calls == 3


def test_gives_up_after_max_attempts_and_never_leaks_the_key():
    embedder = mock(lambda request: httpx.Response(429, text=f"rate limited {FAKE_KEY}"))
    with pytest.raises(EmbeddingError) as err:
        embedder.embed(["x"], "search_query")
    assert err.value.code == "provider_http" and embedder.calls == SMALL.max_attempts
    assert FAKE_KEY not in str(err.value)


def test_auth_errors_are_not_retried():
    embedder = mock(lambda request: httpx.Response(401))
    with pytest.raises(EmbeddingError, match="provider_auth"):
        embedder.embed(["x"], "search_query")
    assert embedder.calls == 1


def test_wrong_dimension_or_count_is_rejected_not_padded():
    with pytest.raises(EmbeddingError, match="invalid_vector"):
        mock(lambda r: httpx.Response(200, json={"embeddings": {"float": [[0.1, 0.2]]}})).embed(["x"], "search_query")
    with pytest.raises(EmbeddingError, match="invalid_response"):
        mock(lambda r: httpx.Response(200, json={"embeddings": {"float": []}})).embed(["x"], "search_query")
    with pytest.raises(EmbeddingError):
        validate_vector([float("nan"), 1.0, 1.0, 1.0], 4)


def test_malformed_success_response_is_reported_without_leaking_body():
    responses = (httpx.Response(200, text="not-json"), httpx.Response(200, json=["unexpected"]))
    for response in responses:
        with pytest.raises(EmbeddingError, match="invalid_response"):
            mock(lambda r, response=response: response).embed(["x"], "search_query")


def test_missing_key_fails_before_any_call():
    with pytest.raises(EmbeddingError, match="missing_key"):
        CohereEmbedder(SMALL, "")


def test_input_text_and_hash():
    text = build_input(PROFILE, "Sleep in autism", "Results > Melatonin", "Melatonin improved sleep onset.")
    assert text == "Sleep in autism\nResults > Melatonin\n\nMelatonin improved sleep onset."
    assert input_hash(PROFILE, text) == input_hash(PROFILE, text)
    assert input_hash(PROFILE, text) != input_hash(replace(PROFILE, vector_dimension=1024), text)
    assert l2_norm([3.0, 4.0]) == 5.0


def test_billed_tokens_are_summed_when_the_provider_reports_them():
    def handler(request: httpx.Request) -> httpx.Response:
        n = len(json.loads(request.content)["texts"])
        return httpx.Response(200, json={"embeddings": {"float": [vector() for _ in range(n)]},
                                         "meta": {"billed_units": {"input_tokens": 7 * n}}})

    client = mock(handler)
    client.embed(["a", "b", "c"], "search_document")
    assert client.billed_input_tokens == 21 and client.calls == 1
