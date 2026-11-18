"""Real FastAPI + research-reader smoke test with a pre-authorized cached evaluation query."""

import pytest
from fastapi.testclient import TestClient

from app.api import create_app

pytestmark = pytest.mark.integration


def test_cached_q001_retrieves_from_authorized_research_view():
    response = TestClient(create_app()).post("/api/retrieve", json={
        "query": "Rối loạn phổ tự kỷ là gì?", "top_k": 5,
    })
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "success" and body["result_count"] == 5
    assert [row["rank"] for row in body["results"]] == [1, 2, 3, 4, 5]
    assert len({row["chunk_id"] for row in body["results"]}) == 5
    assert all(row["source_id"] and row["document_title"] and row["content"] for row in body["results"])
