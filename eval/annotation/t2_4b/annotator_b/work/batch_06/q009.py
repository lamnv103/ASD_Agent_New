import sys; sys.path.insert(0,'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_06')
from lab import write
Z=['EF25F5CC9C','79D6BD3B77','22908472AA','48F25F64E6','17F7212FB3','737D96EBD5','101322C34F','2840626642','DB9335FDF7','A154872691','19DA9189B0','90A2C6E202','94200E0E8B','CD99A2D262','3245E4DE95','96546D8371','66F7C612B6','14AEE772C4','3CBB43DEBC','14ABD88331','CFB20BB28C','A96BDC8631','E646E35687','B2357DD29E','EDBC96ECE7','7456CC3B66','00710AA635','E4C4284AB2','82B2F3231F']
L=[(c,0,'Không đề cập đến việc trẻ không phản ứng khi được gọi tên.','','high') for c in Z]
L+=[
('29AF44F603',3,'Liệt kê không đáp lại khi gọi tên lúc 9 tháng là đặc điểm giao tiếp xã hội liên quan ASD.','Does not respond to name by 9 months of age','high'),
('902F0B5315',1,'Tiêu chí DSM về thiếu đáp ứng xã hội chung, không nêu gọi tên.','failure to initiate or respond to social interactions','low'),
('4E467B4388',1,'Bảng nêu hành vi không nhìn lên khi được nói chuyện ở trẻ ASD hay bỏ đi, chỉ gần với ý hỏi.','Does not look up when spoken to','low'),
('4032D63FB1',1,'Khuyên liên hệ bác sĩ khi lo ngại về hành vi của trẻ, không nói đến gọi tên.','if you think your child might have ASD','low'),
('67B8EF66F0',1,'Nêu dấu hiệu ASD xuất hiện sớm, không nhắc gọi tên.','Many children show symptoms by 12 months to 18 months of age or earlier.','low'),
('B459D6B24E',1,'Hướng dẫn xin đánh giá phát triển, không nói về dấu hiệu gọi tên.','request a free evaluation to find out if your child qualifies for intervention services','low'),
('D38A51B535',1,'Hướng dẫn xin đánh giá miễn phí, không nói về dấu hiệu gọi tên.','to find out if your child qualifies for intervention services','low'),
('37EC0F32E1',1,'Nói chung về khó khăn giao tiếp ở trẻ ASD, không nhắc gọi tên.','Children with ASD may have difficulty developing language skills and understanding what others say to them.','low'),
('61FED4BE44',3,'Nêu trẻ ASD thường không đáp lại lời nói và có thể không đáp khi gọi tên, dễ bị tưởng nhầm là điếc.','They often do not respond to the speech of others and may not respond to their own names.','high'),
('6FD8865DAE',1,'Mô tả ADHD có khó lắng nghe khi được nói trực tiếp, là bối cảnh chẩn đoán phân biệt.','Listening when spoken to directly','low'),
('97607E0A50',3,'Liệt kê không đáp hoặc chậm đáp khi được gọi tên là hành vi thường gặp ở ASD.','Not responding or being slow to respond to one’s name or other verbal bids for attention','high'),
]
write('q009',L)
