"""Mock answer generator for demo/frontend testing only — never calls an external LLM.

Builds a deterministic, clearly-labeled placeholder answer strictly from the evidence excerpts it is
given. It never invents a source or citation beyond what retrieval actually returned, never diagnoses
autism or prescribes treatment, and states explicitly when there is not enough retrieved evidence to
answer. The `MOCK` label and the safety disclaimer are always present in the generated text so the UI
cannot show this output as if it were a real AI-generated clinical answer.
"""

from __future__ import annotations

from dataclasses import dataclass

SAFETY_NOTICE = ("Nguyên mẫu nghiên cứu/sinh viên. Nội dung chưa được thẩm định lâm sàng. "
                  "Không dùng để chẩn đoán hoặc thay thế tư vấn chuyên môn.")
MOCK_HEADER = "[MOCK — câu trả lời minh hoạ để kiểm thử giao diện, KHÔNG phải câu trả lời AI thực tế]"
EXCERPT_MAX_CHARS = 240


@dataclass(frozen=True)
class MockAnswer:
    text: str
    mode: str  # always "mock"
    citation_ids: list[str]
    sufficient_evidence: bool


def _truncate(text: str, limit: int = EXCERPT_MAX_CHARS) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "…"


class MockAnswerGenerator:
    """Demo-only answer text, grounded only in the evidence passed to `generate`. No network calls."""

    def generate(self, query: str, evidence: list[dict]) -> MockAnswer:
        if not evidence:
            text = "\n".join([
                MOCK_HEADER,
                "Không tìm thấy đủ bằng chứng đã truy xuất để trả lời câu hỏi này trong phạm vi dữ liệu hiện có.",
                SAFETY_NOTICE,
            ])
            return MockAnswer(text=text, mode="mock", citation_ids=[], sufficient_evidence=False)

        lines = [MOCK_HEADER, "Trích đoạn bằng chứng đã truy xuất (không phải văn bản do AI tổng hợp):"]
        citation_ids = []
        for item in evidence:
            citation_id = item["citation_id"]
            citation_ids.append(citation_id)
            lines.append(f"{citation_id} {_truncate(item['excerpt'])}")
        lines.append(SAFETY_NOTICE)
        return MockAnswer(text="\n".join(lines), mode="mock", citation_ids=citation_ids, sufficient_evidence=True)
