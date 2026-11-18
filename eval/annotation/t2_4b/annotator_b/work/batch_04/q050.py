from lib import run
R = [
("904B45C2FA", 3, "Cột mốc ngôn ngữ lúc 15 tháng: trẻ thường cố nói một hai từ ngoài mama/dada, trả lời trực tiếp mức kỳ vọng.", "Tries to say one or two words besides “mama” or “dada,”", "high"),
("BEFFDC325B", 3, "Nếu trẻ 15 tháng chưa đạt cột mốc hoặc phụ huynh lo lắng, nên hành động sớm và nói với bác sĩ.", "If your child is not meeting one or more milestones, has lost skills he or she once had, or you have other concerns, act early.", "high"),
("3BF1088600", 2, "Khuyên nói với bác sĩ nếu trẻ không đạt cột mốc, kể cả về nói; không riêng 15 tháng.", "If your child is not meeting the milestones for his or her age", "high"),
("9342A2D354", 2, "Hướng dẫn liên hệ hệ thống can thiệp sớm cho trẻ dưới 3 tuổi khi lo ngại.", "If your child is younger than 3 years old, contact your local early intervention system", "medium"),
("589B23388B", 1, "Cột mốc 18 tháng (3 từ trở lên) giúp so sánh nhưng không phải mốc 15 tháng.", "Tries to say three or more words besides “mama” or “dada”", "medium"),
("F19286CC7C", 1, "Cột mốc ngôn ngữ lúc 2 tuổi, chỉ là bối cảnh tiến triển.", "Says at least two words together, like “More milk.”", "medium"),
("C8E5C9A43B", 1, "Lời khuyên chung hành động sớm nhưng ở mốc 2 tháng.", "If your child is not meeting one or more milestones, has lost skills he or she once had, or you have other concerns, act early.", "low"),
("3A3BEDE2E6", 1, "Hướng dẫn xin chuyển chuyên khoa/can thiệp sớm nếu còn lo ngại, ở mốc 2 tháng.", "Ask for a referral to a specialist who can evaluate your child more", "low"),
("374F9F7424", 1, "Mẹo giúp trẻ 15 tháng học nói, không trả lời có đáng lo hay không.", "Help your child learn to speak.", "medium"),
("7B6605905D", 1, "Nêu bảng kiểm cột mốc 15 tháng để theo dõi, không có nội dung về lời nói.", "Check the milestones your child has reached by 15 months by completing a checklist", "medium"),
("BEEF56329D", 1, "Tổng quan trang cột mốc 15 tháng, nhắc thông tin chia sẻ với bác sĩ.", "See important information to share with your doctor.", "low"),
("C7E5EC78FE", 1, "Mẹo kích thích nói và cử chỉ ở trẻ 15 tháng, chỉ gián tiếp.", "Continue to talk, read, sing, and tell your child the names of things throughout the day.", "medium"),
("579BE65BFF", 1, "Nói về đánh giá ngôn ngữ ở trẻ nghi ASD, trẻ thiếu kỹ năng tiền ngôn ngữ nên được đánh giá; không nêu mốc 15 tháng.", "Children who lack these skills may be evaluated and treated by a speech-language pathologist to prevent further developmental delays.", "medium"),
]
run('q050', R, default_zero="Không trả lời việc trẻ 15 tháng chưa nói từ nào có đáng lo hay không.")
