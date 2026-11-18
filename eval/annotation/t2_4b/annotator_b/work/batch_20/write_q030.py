import json
import sys

sys.path.insert(0, 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_20')
from verify_question import get_question_passages
passages = get_question_passages('D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/batches/batch_20.jsonl', 'q030')

# Q030: Trẻ tự kỷ có hay gặp vấn đề tiêu hóa không?
# 39 candidates

annotations_q030_raw = [
    # 1. E9011AA1B7 - Table 1 of systematic review: study details showing GIS prevalence in ASD (Prosperi: 40.5%, Restrepo, Reynolds)
    {
        'annotation_code': 'E9011AA1B7',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các nghiên cứu báo cáo tỷ lệ và loại triệu chứng tiêu hóa ở trẻ tự kỷ, cung cấp số liệu thực nghiệm hỗ trợ trả lời câu hỏi.',
        'target_span': 'At least one severe GI symptom or FS in 40.5% of participants.',
        'confidence': 'high'
    },
    # 2. 059E6E38A4 - Table 1 (Rose, Sanctuary, Shaaban, Thuslai, Tomova): biological signatures, treatment tolerability, fecal microbiota
    {
        'annotation_code': '059E6E38A4',
        'grade': 1,
        'rationale': 'Bảng tóm tắt các nghiên cứu can thiệp vi sinh và điều trị triệu chứng tiêu hóa ở trẻ tự kỷ, chỉ liên quan gián tiếp đến khía cạnh can thiệp chứ không trực tiếp nêu tần suất mắc bệnh.',
        'target_span': 'The participants demonstrated strong positive correlation of ASD severity with the severity of GI dysfunction.',
        'confidence': 'high'
    },
    # 3. 27A5051F0B - Constipation rates, food selectivity, 5-fold increased risk of feeding problems
    {
        'annotation_code': '27A5051F0B',
        'grade': 3,
        'rationale': 'Đoạn nêu rõ tỷ lệ táo bón tăng ở trẻ tự kỷ, nguy cơ gặp vấn đề ăn uống cao gấp 5 lần so với bạn bè đồng trang lứa và mối liên hệ với rối loạn chức năng tiêu hóa.',
        'target_span': 'Autistic children have a fivefold increased risk of developing feeding problems when compared to typically developing peers[96].',
        'confidence': 'high'
    },
    # 4. 39E1490098 - GIS and challenging behavior in ASD (Ferguson et al., older vs younger)
    {
        'annotation_code': '39E1490098',
        'grade': 2,
        'rationale': 'Đoạn thảo luận về sự xuất hiện của các triệu chứng tiêu hóa (buồn nôn, táo bón, đau bụng) ở trẻ tự kỷ và mối tương quan với hành vi thách thức.',
        'target_span': 'The presence of challenging behaviors may reflect the expression of abdominal discomfort in preschool children with ASD [48].',
        'confidence': 'high'
    },
    # 5. 926FB2C02F - Integrated microbiome-metabolome analyses in ASD associate with GI symptoms
    {
        'annotation_code': '926FB2C02F',
        'grade': 1,
        'rationale': 'Đoạn đề cập đến phân tích vi hệ vi sinh và chất chuyển hóa liên quan đến triệu chứng tiêu hóa ở người tự kỷ dưới góc độ cơ chế sinh học phân tử.',
        'target_span': 'Integrated microbiome–metabolome analyses (fecal SCFAs, bile acids, aromatic amino acid catabolites) reveal distinct clusters in ASD that associate with GI symptoms and adaptive behavior [143].',
        'confidence': 'high'
    },
    # 6. 425E4D27A0 - Immune response, autoimmune conditions in autism. Mentions celiac, Crohn not statistically significant.
    {
        'annotation_code': '425E4D27A0',
        'grade': 1,
        'rationale': 'Đoạn bàn về tình trạng miễn dịch và bệnh tự miễn ở trẻ tự kỷ, có nhắc tới việc không tìm thấy tương quan thống kê với bệnh celiac hay Crohn, là khía cạnh gián tiếp.',
        'target_span': 'Neither of these studies found a statistical correlation between celiac disease, Crohn’s disease, and autism.',
        'confidence': 'high'
    },
    # 7. 6FCCC35532 - Table 2: Key factors and association to GIS. Positive association with presence of ASD.
    {
        'annotation_code': '6FCCC35532',
        'grade': 3,
        'rationale': 'Bảng tổng hợp cho thấy sự liên hệ đồng thuận rõ ràng giữa sự hiện diện của tự kỷ (Presence of ASD) và các triệu chứng tiêu hóa (GIS).',
        'target_span': '| Positive Association | Presence of ASD [8,24,26]. |',
        'confidence': 'high'
    },
    # 8. FBA481F73E - The prevalence and nature of GIS in ASD: 30-37%, 43%, up to 82%, 2-3x higher than TD
    {
        'annotation_code': 'FBA481F73E',
        'grade': 3,
        'rationale': 'Đoạn cung cấp số liệu dịch tễ cụ thể về tỷ lệ mắc triệu chứng tiêu hóa ở trẻ tự kỷ (30-82.4%) và khẳng định trẻ tự kỷ có nguy cơ mắc cao gấp 2-3 lần trẻ phát triển bình thường.',
        'target_span': 'The studies in this review found that children with ASD are significantly more likely to experience GIS than control groups and children with typical development (TD) [8,24,26].',
        'confidence': 'high'
    },
    # 9. 194294C1C1 - GIS and sleep problems in ASD (Neumeyer, Yang, McCue)
    {
        'annotation_code': '194294C1C1',
        'grade': 2,
        'rationale': 'Đoạn thảo luận về mối liên hệ giữa các vấn đề tiêu hóa (như táo bón) và rối loạn giấc ngủ ở trẻ tự kỷ, cho thấy các vấn đề tiêu hóa là đồng mắc phổ biến.',
        'target_span': 'The results of the study indicated that the adjusted odds ratio for sleep disorders amongst GI dysfunctions compared with those without GI dysfunctions was 1.74 (95% CI: 1.22–2.48).',
        'confidence': 'high'
    },
    # 10. C90EC7688D - Types and prevalence of GIS in ASD (reflux, nausea, vomiting, constipation, diarrhea, pain)
    {
        'annotation_code': 'C90EC7688D',
        'grade': 3,
        'rationale': 'Đoạn trình bày chi tiết tỷ lệ các vấn đề tiêu hóa cụ thể ở trẻ tự kỷ như táo bón (22-65%), tiêu chảy (10-64%), đau bụng (22-53%), nôn mửa và buồn nôn.',
        'target_span': 'Constipation occurred in 22.1–24.1% of children with ASD in some samples [46,48] and 47.1–65% in other samples [14,24,41,50].',
        'confidence': 'high'
    },
    # 11. CE7CC34D78 - Table 1 (Vargason, Williams, Yang, Zickgraf: antibiotics, anxiety, GIS, atypical eating & constipation 70.5%)
    {
        'annotation_code': 'CE7CC34D78',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các nghiên cứu về mối liên hệ giữa tự kỷ, triệu chứng tiêu hóa và hành vi ăn uống bất thường (táo bón liên quan đến hành vi ăn uống ở 70.5% trẻ ASD).',
        'target_span': 'ASD + GIS associated with more severe ASD core symptoms than those without GIS.',
        'confidence': 'high'
    },
    # 12. ADC9693B49 - ADHD and anxiety symptoms in ASD. No mention of GI.
    {
        'annotation_code': 'ADC9693B49',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về sự đồng mắc của ADHD và lo âu ở trẻ tự kỷ, hoàn toàn không đề cập đến vấn đề tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 13. EDAD97AF70 - Narrative review on GI CCs in autism: greater risk exists for abdominal pain, diarrhea, constipation
    {
        'annotation_code': 'EDAD97AF70',
        'grade': 3,
        'rationale': 'Đoạn khẳng định tổng quan y văn cho thấy trẻ tự kỷ có nguy cơ cao hơn gặp các vấn đề tiêu hóa như đau bụng, tiêu chảy, táo bón so với thông thường.',
        'target_span': 'Review of the scientific literature does indicate that a greater risk for GI concerns (e.g., abdominal pain, diarrhea, constipation) exists in these patients, though the etiology of these observations remains unclear.',
        'confidence': 'high'
    },
    # 14. 5F3225C646 - Autism in Vietnam: scoping review, stigma.
    {
        'annotation_code': '5F3225C646',
        'grade': 0,
        'rationale': 'Đoạn nói về sự kỳ thị và bối cảnh tự kỷ tại Việt Nam, không liên quan đến vấn đề tiêu hóa ở trẻ tự kỷ.',
        'target_span': '',
        'confidence': 'high'
    },
    # 15. F0A63C3885 - GIS prevalence by gender, age, persistence over time in ASD
    {
        'annotation_code': 'F0A63C3885',
        'grade': 3,
        'rationale': 'Đoạn nêu tỷ lệ triệu chứng tiêu hóa ở trẻ tự kỷ theo giới tính (bé gái 97.1%, bé trai 87.6%) và chỉ ra rằng các triệu chứng tiêu hóa kéo dài liên tục theo thời gian.',
        'target_span': 'Babinska et al. [24] found GIS more common in girls with ASD than in boys (97.1% to 87.6% 2 = 13.57, p = 0.009), and 70.6% of girls and 44.5% of boys experienced GIS several times weekly or every day.',
        'confidence': 'high'
    },
    # 16. 166EDD7E41 - Autism in Vietnam: participatory research methods.
    {
        'annotation_code': '166EDD7E41',
        'grade': 0,
        'rationale': 'Đoạn nghiên cứu về sự tham gia của cộng đồng vào các nghiên cứu tự kỷ ở Việt Nam, không liên quan đến vấn đề tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 17. CD2D552C6D - Table 1 (Mazefsky, McCue, Neuhaus, Neumeyer: sleep, constipation, psychiatric symptoms)
    {
        'annotation_code': 'CD2D552C6D',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các nghiên cứu ghi nhận mối liên hệ giữa vấn đề tiêu hóa (GIS, táo bón) với rối loạn giấc ngủ và triệu chứng cảm xúc ở trẻ tự kỷ.',
        'target_span': 'Sign more sleep disorder s/s for children with GI problems (64.1%; 150/234) than for those without GI problems (50.8%; 156/307).',
        'confidence': 'high'
    },
    # 18. 58A0FA8F8D - Assessment of ASD: diagnostic criteria, DSM-5-TR.
    {
        'annotation_code': '58A0FA8F8D',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về các tiêu chuẩn chẩn đoán tự kỷ theo DSM-5-TR, không đề cập đến vấn đề tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 19. 94769E88C7 - Elopement/wandering in children with DD in US.
    {
        'annotation_code': '94769E88C7',
        'grade': 0,
        'rationale': 'Đoạn bàn về hành vi đi lang thang (elopement) ở trẻ có khuyết tật phát triển, hoàn toàn không liên quan đến vấn đề tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 20. C40FC9B9B9 - Anxiety and motor skills in ASD and ADHD.
    {
        'annotation_code': 'C40FC9B9B9',
        'grade': 0,
        'rationale': 'Đoạn bàn về mức độ lo âu và kỹ năng vận động ở trẻ tự kỷ và ADHD, không nhắc đến tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 21. A7735C28D7 - GIS and challenging behaviors, psychopathology, sensory issues in ASD
    {
        'annotation_code': 'A7735C28D7',
        'grade': 2,
        'rationale': 'Đoạn thảo luận về việc triệu chứng tiêu hóa xuất hiện ở 40-65% trẻ tự kỷ có kèm triệu chứng tiêu hóa và liên hệ với các vấn đề lo âu, cảm giác.',
        'target_span': 'Challenging behaviors are common, and they occur in between 40% and 65% of children with ASD who have at least one GIS [14,44,48].',
        'confidence': 'high'
    },
    # 22. E76806EA1E - ADHD and anxiety in ASD: adaptive functioning.
    {
        'annotation_code': 'E76806EA1E',
        'grade': 0,
        'rationale': 'Đoạn về lo âu và chức năng thích nghi ở trẻ tự kỷ có đồng mắc ADHD, không liên quan đến tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 23. 4F759C9754 - GIS etiology in ASD, literature review (Mannion & Leader: 28 studies)
    {
        'annotation_code': '4F759C9754',
        'grade': 2,
        'rationale': 'Đoạn thảo luận y văn về mối liên hệ giữa triệu chứng tiêu hóa với sự thoái lui ngôn ngữ và mức độ nghiêm trọng của tự kỷ, cung cấp cái nhìn tổng quan về GIS ở trẻ tự kỷ.',
        'target_span': 'A literature review by Mannion and Leader examined twenty-eight studies that focused on the relationship between GIS and developmental regression, language, ASD severity, challenging behavior, comorbid psychopathology, sleep problems, and sensory issues [4].',
        'confidence': 'high'
    },
    # 24. 456574E812 - Challenging behavior and GIS, pica in ASD (associated with vomiting, diarrhea)
    {
        'annotation_code': '456574E812',
        'grade': 2,
        'rationale': 'Đoạn chỉ ra rằng trẻ mẫu giáo tự kỷ có vấn đề tiêu hóa biểu hiện nhiều triệu chứng hành vi hơn, và hội chứng pica ở 9.7% trẻ tự kỷ liên quan đến nôn, tiêu chảy.',
        'target_span': 'Preschool children with ASD with GIS were found to have substantially more internalizing and externalizing symptoms, significantly different emotional/behavioral problems, and restrictive/repetitive behaviors than those without GIS [48].',
        'confidence': 'high'
    },
    # 25. C14F9C0B4B - Table 1 (Esposito, Ferguson, Fields, Fulceri: pica, anxiety, GIS prevalence)
    {
        'annotation_code': 'C14F9C0B4B',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các nghiên cứu cho thấy sự gia tăng các triệu chứng tiêu hóa ở trẻ tự kỷ ngay cả khi không có pica, và mối liên quan với lo âu và vấn đề hành vi.',
        'target_span': 'Without pica, increased GIS is still evident in ASD.',
        'confidence': 'high'
    },
    # 26. B4A6333C97 - GIS, food refusal, sensory issues, Clostridium difficile in ASD
    {
        'annotation_code': 'B4A6333C97',
        'grade': 1,
        'rationale': 'Đoạn khảo sát mối liên hệ giữa vi khuẩn đường ruột (C. difficile), rối loạn cảm giác và triệu chứng tiêu hóa ở trẻ tự kỷ.',
        'target_span': 'They found that sensory issues were a partial predictor of food selectivity, which was common and exhibited by 84.6% of their sample. GIS were predictive of chewing problems, rapid eating, and vomiting.',
        'confidence': 'high'
    },
    # 27. C343FC4573 - Narrative review: most common GI concerns in ASD (constipation, diarrhea, abdominal pain) are more common than in neurotypical peers
    {
        'annotation_code': 'C343FC4573',
        'grade': 3,
        'rationale': 'Đoạn khẳng định các vấn đề tiêu hóa phổ biến nhất ở người tự kỷ (táo bón, tiêu chảy, đau bụng) đều xuất hiện thường xuyên hơn ở trẻ tự kỷ so với trẻ phát triển bình thường.',
        'target_span': 'The most common GI concerns among autistic individuals include constipation, diarrhea, and abdominal pain, all of which have been found to be more common among autistic children compared to neurotypical peers[10,96].',
        'confidence': 'high'
    },
    # 28. 7A2E5461C6 - Table 1 (Babinska, Bresnahan, Chaidez: prevalence of GIS, food selectivity)
    {
        'annotation_code': '7A2E5461C6',
        'grade': 3,
        'rationale': 'Bảng tóm tắt các nghiên cứu quy mô lớn cho thấy các bà mẹ có con tự kỷ có tỷ lệ báo cáo táo bón và dị ứng thực phẩm cao hơn có ý nghĩa thống kê so với trẻ bình thường.',
        'target_span': 'Mothers of children with ASD were significantly more likely to report constipation, food allergy/intolerance in the 6–18 month and diarrhea, constipation and food allergy/intolerance in the 18–36 month periods.',
        'confidence': 'high'
    },
    # 29. DC9136F2EE - Table 1 (Ghalichi, Grimaldi, Jiang: GI abnormalities in 53.9%, prebiotic/gluten-free diet)
    {
        'annotation_code': 'DC9136F2EE',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các thử nghiệm can thiệp báo cáo bất thường tiêu hóa xuất hiện ở 53.9% trẻ tự kỷ trong nghiên cứu của Ghalichi et al.',
        'target_span': 'GI abnormalities in 53.9%. In the gluten-free diet group, the prevalence of GIS decreased significantly to 17.10%.',
        'confidence': 'high'
    },
    # 30. 5FF118BF59 - Fecal DNA, gut microbiome alterations, elimination diets in ASD
    {
        'annotation_code': '5FF118BF59',
        'grade': 1,
        'rationale': 'Đoạn thảo luận về sự khác biệt trong hệ vi sinh đường ruột và các can thiệp chế độ ăn kiêng ở trẻ tự kỷ có vấn đề tiêu hóa, mang tính chất cơ chế sinh học.',
        'target_span': 'Prior studies of fecal DNA suggest that certain bacterial clusters are overrepresented in autistic children and GI complaints when compared to neurotypical peers with similar clinical concerns[105].',
        'confidence': 'high'
    },
    # 31. D5089990C0 - Gut microbiota differences (Rose, Tomova, Shaaban: chronic gut inflammation, Desulfovibrio)
    {
        'annotation_code': 'D5089990C0',
        'grade': 1,
        'rationale': 'Đoạn trình bày bằng chứng về sự khác biệt của hệ vi sinh đường ruột và viêm ruột mạn tính ở trẻ tự kỷ có vấn đề tiêu hóa, thuộc cơ chế bệnh sinh.',
        'target_span': 'The participants demonstrated a strong positive correlation of ASD severity with the severity of GI dysfunction.',
        'confidence': 'high'
    },
    # 32. 5D0199C5DE - GI problems frequently reported among autistic children, atypical presentation
    {
        'annotation_code': '5D0199C5DE',
        'grade': 3,
        'rationale': 'Đoạn mở đầu khẳng định các vấn đề tiêu hóa thường xuyên được báo cáo ở trẻ tự kỷ và đóng góp đáng kể vào gánh nặng bệnh tật của trẻ.',
        'target_span': 'GI problems are frequently reported among autistic children. These conditions contribute significantly to the disease burden associated with autism, though estimates of their prevalence vary substantially due to differences in sampling and measurement',
        'confidence': 'high'
    },
    # 33. EAC79F1FBE - Table 1 (Kang, Khalil, Leader, Mannion: MTT, GIS persisted in 84.4%)
    {
        'annotation_code': 'EAC79F1FBE',
        'grade': 2,
        'rationale': 'Bảng tóm tắt các nghiên cứu can thiệp và theo dõi dọc ghi nhận triệu chứng tiêu hóa kéo dài ở 84.4% người tham gia tự kỷ.',
        'target_span': 'GIS persisted in 84.4% of participants and 92.9% had family history of autoimmune disease.',
        'confidence': 'high'
    },
    # 34. 969DF97C3D - GIS and sleep problems in ASD (odds of sleep disorder increased by 68%)
    {
        'annotation_code': '969DF97C3D',
        'grade': 1,
        'rationale': 'Đoạn thảo luận về sự gia tăng nguy cơ rối loạn giấc ngủ ở trẻ tự kỷ có rối loạn tiêu hóa, cung cấp bối cảnh về hậu quả của vấn đề tiêu hóa.',
        'target_span': 'The evidence suggests that there is a 68% increase in the odds of an autistic child with GI dysfunction, regardless of age and gender, having at least one sleep disorder symptom in comparison to children who do not have GIS [45].',
        'confidence': 'high'
    },
    # 35. 971D19FDAF - Food selectivity and GIS in ASD (constipation related to atypical eating)
    {
        'annotation_code': '971D19FDAF',
        'grade': 2,
        'rationale': 'Đoạn chỉ ra mối liên hệ giữa chọn lọc thực phẩm và việc có ít nhất một triệu chứng tiêu hóa, trong đó táo bón liên quan đến hành vi ăn uống không điển hình.',
        'target_span': 'Food selectivity has been associated with the presence of at least one GIS, higher levels of SIB, and anxiety problems (p < 0.001 Cohen’s d = 0.65) [48].',
        'confidence': 'high'
    },
    # 36. 037ED32C69 - Discussion on anxiety and ADHD in ASD.
    {
        'annotation_code': '037ED32C69',
        'grade': 0,
        'rationale': 'Đoạn thảo luận về mức độ lo âu và đồng mắc tâm thần ở trẻ tự kỷ và ADHD, không liên quan đến tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 37. CB9EFC00A7 - Medical interventions: GFCF diet efficacy in ASD with gastrointestinal symptoms
    {
        'annotation_code': 'CB9EFC00A7',
        'grade': 2,
        'rationale': 'Đoạn nêu hiệu quả của chế độ ăn GFCF ở trẻ tự kỷ có biểu hiện các triệu chứng tiêu hóa (táo bón và tiêu chảy), đề cập đến trẻ có cơ địa bất thường về tiêu hóa.',
        'target_span': 'The authors found that the diet was effective in improving the behaviors of children with ASD showing gastrointestinal symptoms (in particular, constipation and diarrhea) compared to children without GID',
        'confidence': 'high'
    },
    # 38. 099D6157BE - ADHD and anxiety symptoms in ASD: introduction.
    {
        'annotation_code': '099D6157BE',
        'grade': 0,
        'rationale': 'Đoạn giới thiệu về tự kỷ và các rối loạn đồng mắc như ADHD và lo âu, không có thông tin về vấn đề tiêu hóa.',
        'target_span': '',
        'confidence': 'high'
    },
    # 39. AE5889632A - Introduction to GIS in ASD: 9-91% of children with ASD experience GIS, greater risk
    {
        'annotation_code': 'AE5889632A',
        'grade': 3,
        'rationale': 'Đoạn khẳng định trẻ tự kỷ có nguy cơ cao hơn gặp các triệu chứng tiêu hóa (táo bón, tiêu chảy, đau bụng), với tỷ lệ từ 9% đến 91% trẻ tự kỷ gặp các triệu chứng này.',
        'target_span': 'Individuals with ASD frequently have comorbidities [2] and they are at greater risk of experiencing co-occurring gastrointestinal (GI) symptoms, including constipation, diarrhea, and abdominal pain [3]. GIS are experienced by between 9 and 91% of children with ASD',
        'confidence': 'high'
    },
]

# Verify all spans exist in passages
errors = 0
annotations_q030 = []
for item in annotations_q030_raw:
    code = item['annotation_code']
    grade = item['grade']
    target_span = item['target_span']
    
    if grade != 0:
        if target_span not in passages[code]:
            print(f"ERROR: target span not in passage for {code}!")
            print(repr(target_span))
            errors += 1
    else:
        target_span = ""
        
    ann = {
        'annotation_code': code,
        'grade': grade,
        'rationale': item['rationale'],
        'evidence_span': target_span,
        'confidence': item['confidence'],
        'needs_review': False,
        'review_note': '',
        'annotation_type': 'ai_generated',
        'model': 'claude-sonnet-4-6',
        'prompt_version': 't2_4b_ai_v1'
    }
    annotations_q030.append(ann)

if errors == 0:
    outpath = 'D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_20/q030.jsonl'
    with open(outpath, 'w', encoding='utf-8') as f:
        for ann in annotations_q030:
            f.write(json.dumps(ann, ensure_ascii=False) + '\n')
    print(f'Successfully wrote {len(annotations_q030)} annotations to q030.jsonl')
else:
    print(f'Cannot write: {errors} span errors.')
