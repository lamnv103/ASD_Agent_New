# Hướng dẫn chấm relevance (T2.4-B) — bản dành cho người chấm

Bạn nhận một file gồm các cặp **(câu hỏi, đoạn tài liệu)**. Với mỗi cặp, đánh giá đoạn tài liệu giúp trả lời **đúng câu hỏi đó** đến mức nào. Đánh giá theo chính câu hỏi, không theo chủ đề chung của tài liệu.

## Quy tắc độc lập (bắt buộc)
- Chấm một mình. Không trao đổi hay xem nhãn của người chấm khác cho đến khi cả hai đã nộp bài.
- Không dùng AI, chatbot hay công cụ dịch máy để gợi ý nhãn. Được tra từ điển thuật ngữ.
- File của bạn không cho biết đoạn văn được tìm ra bằng cách nào và không có thứ hạng. Đừng cố suy đoán điều đó.
- Thứ tự câu hỏi và đoạn văn đã được xáo trộn ngẫu nhiên. Vị trí trong file không mang ý nghĩa gì.

## Thang điểm
| Grade | Ý nghĩa | Ví dụ |
|---|---|---|
| **3** | Rất liên quan: bằng chứng trực tiếp, quan trọng để trả lời | (ví dụ minh hoạ, không có trong bộ câu hỏi) Câu "Trẻ tự kỷ có hay bị viêm tai giữa không?" và đoạn nêu tỷ lệ viêm tai giữa ở trẻ tự kỷ |
| **2** | Liên quan: liên quan rõ ràng, hỗ trợ trả lời | Đoạn nói viêm tai giữa là vấn đề thường gặp ở trẻ tự kỷ, không có số liệu |
| **1** | Liên quan một phần: chỉ là bối cảnh, gián tiếp, hoặc chỉ một khía cạnh nhỏ | Đoạn về các bệnh tai mũi họng nói chung ở trẻ em, không riêng trẻ tự kỷ |
| **0** | Không liên quan | Đoạn về một chủ đề khác, trang bản quyền, bảng không liên quan |
| **−1** | Mâu thuẫn: nội dung trái với bằng chứng liên quan khác hoặc với kết luận chính, và câu trả lời cần nêu sự mâu thuẫn này | Một đoạn đưa ra kết quả ngược với kết luận chính được nêu ở nơi khác |

**Lưu ý:**
- **−1 không phải "tệ hơn 0".** Đó là một loại bằng chứng riêng, chỉ dùng khi đoạn văn thực sự liên quan nhưng mâu thuẫn.
- **Đoạn dành cho dân số chung** (không riêng trẻ tự kỷ) mà câu hỏi hỏi về trẻ tự kỷ: thường là 1. Chỉ cho 2 nếu đoạn văn tự nói nội dung áp dụng cho trẻ tự kỷ.
- **Câu hỏi không nên trả lời** (ví dụ xin chỉ định riêng cho một trẻ): vẫn chấm theo việc đoạn văn có chứa đúng thông tin được hỏi hay không.
- **Câu hỏi ngoài phạm vi** (không liên quan tự kỷ hay phát triển trẻ): chấm như mọi câu khác. Đoạn không chứa thông tin được hỏi thì là 0.
- Không chấm theo tiêu đề tài liệu: phải đọc nội dung. Trùng từ khoá không có nghĩa là liên quan. Khác cách diễn đạt không có nghĩa là không liên quan.
- Không suy luận y khoa ngoài nội dung đoạn văn.

## Các cột phải điền
| Cột | Bắt buộc | Cách điền |
|---|---|---|
| `grade` | Có, trừ khi chọn `needs_review` | Một trong: −1, 0, 1, 2, 3 |
| `rationale` | Có (khi có grade) | 1–2 câu, kiểm chứng được bằng cách đọc lại đoạn văn |
| `evidence_span` | Có khi grade là 1, 2, 3 hoặc −1 | **Chép nguyên văn** một đoạn ngắn trong cột `content` làm căn cứ (validator sẽ kiểm tra đoạn này có trong nội dung) |
| `confidence` | Có (khi có grade) | `high`, `medium` hoặc `low` |
| `needs_review` | Khi không đủ thông tin để kết luận | Ghi `yes` và để trống `grade`. **Không đoán** |
| `review_note` | Có khi `needs_review` = yes | Vì sao cần chuyên gia, ví dụ "không chắc thuật ngữ trong đoạn văn có cùng nghĩa với khái niệm trong câu hỏi không" |

Không xoá hay sửa các cột `annotation_code`, `question_id`, `question_vi` và `content`. Cặp nào bạn chưa chấm thì để trống: cặp đó sẽ được tính là **chưa chấm**, không bao giờ bị tính là 0.

## Ước lượng khối lượng
Mỗi file có 2.791 cặp thuộc 66 câu hỏi (trung bình 42 cặp mỗi câu; đoạn văn dài tối đa khoảng 3.800 ký tự). Với khoảng 1 phút mỗi cặp, tổng cộng khoảng **45–50 giờ** cho mỗi người. Nên chấm theo từng câu hỏi và nghỉ giữa các phiên.
