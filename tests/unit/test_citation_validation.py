from app.retrieval.citation_validation import validate
from app.retrieval.types import RetrievedChunk

CHUNK = RetrievedChunk(
    rank=1, chunk_id="c1", source_id="S1", document_id="D1", title="Real Title", source_url="https://real",
    content="real content", content_sha256="h", section="Sec", page="4", char_range=None,
    score_type="cosine_distance", score=0.3, cosine_similarity=0.7, authorization_version=1,
    embedding_profile="p", model_id="m", corpus_version="v1",
)


def good_item(**changes):
    item = {"citation_id": "C1", "source_id": "S1", "title": "Real Title", "section": "Sec", "page": "4",
            "char_range": None, "source_url": "https://real", "excerpt": "real content", "rank": 1}
    return item | changes


def test_a_citation_matching_the_actual_retrieved_chunk_passes():
    assert validate([good_item()], [CHUNK]) == [good_item()]


def test_a_citation_not_in_the_supported_set_is_dropped():
    # citation_id "C2" never appeared among the chunks the Evidence Gate judged supporting.
    assert validate([good_item(citation_id="C2")], [CHUNK]) == []


def test_a_fabricated_url_is_dropped_even_if_everything_else_matches():
    assert validate([good_item(source_url="https://fabricated")], [CHUNK]) == []


def test_a_fabricated_title_is_dropped():
    assert validate([good_item(title="Made Up Title")], [CHUNK]) == []


def test_altered_excerpt_text_is_dropped():
    assert validate([good_item(excerpt="this text was never actually retrieved")], [CHUNK]) == []


def test_empty_inputs_validate_to_empty():
    assert validate([], []) == []
