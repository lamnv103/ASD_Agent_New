import json, sys

src = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_19/q016.txt"
with open(src, "r", encoding="utf-8") as f:
    text = f.read()

parts = text.split("\n### ")
blocks = {}
for p in parts[1:]:
    code = p[:10]
    rest = p[len(code):]
    nl = rest.find("\n")
    content = rest[nl:].strip()
    blocks[code] = content

labels = {
"FDAA21B5C4": (1, "Chi la bang giai thich tu viet tat IJA, JASP lien quan chu y chung.", "IJA: Initiating Joint Attention", "medium", False, ""),
"46AA2018C5": (2, "Lieu trinh P-ESDM qua dao tao cha me co muc tieu thuc day chu y chung.", "Facilitating joint attention", "medium", False, ""),
"959562719E": (0, "Bang yeu to PRT chung, khong noi ve chu y chung.", "", "high", False, ""),
"1C81D20699": (3, "JASP nham vao chu y chung, hoat dong choi co cau truc giup tap chu y chung.", "JASP targeted joint attention, engagement, and symbolic play, while EMT focused on modeling and prompting language in natural routines.", "high", False, ""),
"2541E28AED": (2, "Huong dan cha me cach xay dung su chu y chia se qua choi va thuong ngay.", "Children have more opportunities to learn when they are sharing engagement \u2013 noticing you and your activity.", "medium", False, ""),
"C1F1910E90": (1, "Chi neu PMI co tac dong tich cuc den chu y chung, khong giai thich chi tiet.", "emphasized the positive effect of PMIs on joint attention and social interaction in the parent-child dyad", "medium", False, ""),
"94F3C602A3": (2, "Huong dan ky thuat bat chuoc, cung choi de xay dung su chu y chia se.", "Look and listen to your child\u2019s actions and join in the routine by doing the same thing as your child.", "medium", False, ""),
"558F019292": (0, "Chi noi tieu chuan loai tru do luong chu y chung trong nghien cuu, khong giai thich.", "", "high", False, ""),
"41F88093F5": (1, "Chi nhac chu y chung la mot muc tieu cu the cua can thiep qua cha me.", "others targeting specific impairments, e.g., joint attention, communication, or language", "medium", False, ""),
"3CABAF4D3F": (2, "So sanh JASPER va DTT cho thay tre co chu y chung tot hon loi hon tu JASPER.", "children with stronger receptive language and joint attention benefited more from JASPER", "medium", False, ""),
"097975A837": (0, "Noi ve xu ly hanh vi thach thuc, khong lien quan chu y chung.", "", "high", False, ""),
"9517648800": (0, "Noi ve xu ly hanh vi thach thuc, khong lien quan chu y chung.", "", "high", False, ""),
"B13ED61DEB": (2, "Nghien cuu ve khoi xuong/dap lai chu y chung va chuong trinh mau giao cai thien no.", "after a preschool program focused on joint attention and joint engagement, improvements in the initiation of joint attention with peers were achieved", "medium", False, ""),
"F4CFF3500D": (2, "Giai thich su chia se chu y la cung chu y nguoi va hoat dong, qua vi du thuc te.", "Shalini wants Viran to share engagement (pay attention to her and to a shared activity at the same time) which is the best for learning.", "medium", False, ""),
"FA0DB22257": (0, "Chi la meo thu hut tre choi chung, khong noi ve chu y chung.", "", "high", False, ""),
"263E7EEA2E": (2, "P-ESDM day cha me ky nang chu y chung va bat chuoc de tang tuong tac xa hoi.", "certified ESMD trainers teach parent-specific behavioral skills, such as joint attention and imitation, to facilitate social interaction with their child.", "medium", False, ""),
"4D13C2ABF3": (1, "Bang ket qua cho thay can thiep khong cai thien ro chu y chung, du lieu le.", "No significant improvements in joint attention or behavioral regulation.", "medium", False, ""),
"3C732384A4": (1, "Cau chuyen cha me bat chuoc con choi, lien quan gian tiep den xay dung chu y chung.", "the way to play is to look and listen to find out what he is interested in. I can imitate what he does with the toys", "medium", False, ""),
"EA0E2C6751": (0, "Noi ve xu ly hanh vi thach thuc de thu hut chu y, khong ve chu y chung.", "", "high", False, ""),
"761E3944AB": (0, "Noi ve ADHD, khong lien quan chu y chung.", "", "high", False, ""),
"F96209B780": (0, "Meo khen ngoi tre, khong de cap chu y chung.", "", "high", False, ""),
"5FED33BA73": (1, "Chi la bang giai thich tu viet tat JASP lien quan chu y chung.", "JASP Joint Attention, Symbolic Play", "medium", False, ""),
"B20898757A": (2, "Bang nghien cuu neu ten mot can thiep goi la 'Joint attention intervention' va hieu qua.", "Joint attention intervention", "medium", False, ""),
"63B057BBB6": (2, "Cong cu CBRSi do chu y chung, ket qua cho thay chu y/khoi xuong cua tre tang.", "CBRSi[52]\u2014measures engagement and interest in activity as well as joint attention, creativity, and affect demonstrated toward the parent.", "medium", False, ""),
"FC62DC7DDA": (2, "Tong hop cho thay JASPER/SGD cai thien chu y chung o nhieu nghien cuu khac nhau.", "Almirall et al. [48] and Kasari et al. [55] reported improved joint attention with SGD/JASPER", "medium", False, ""),
"34C8803220": (1, "Chi nhac can thiep nham vao chu y chung la mot trong cac muc tieu.", "the intervention targeted specific areas of ASD (such as joint attention and social-communicative skills)", "medium", False, ""),
"6335221551": (2, "Phan tich chu y chung la chuc nang xa hoi hay cong cu, giai thich khai niem ro.", "Rice et al. (2016) distinguished the aims of joint attention and joint engagement as social versus instrumental functions", "medium", False, ""),
"D30AD678C2": (3, "Dinh nghia cap do chu y: chia se chu y la cung luu y nguoi va hoat dong, co vi du.", "These children are sharing engagement with someone (noticing a person and doing a shared activity at the same time).", "high", False, ""),
"272E37EB16": (3, "Dinh nghia ro: chia se chu y la tre chu y hai thu cung luc - nguoi lon va hoat dong.", "Shared engagement means that the child is paying attention to two things at the same time:", "high", False, ""),
"65616D0197": (1, "Chi la bang giai thich tu viet tat JASPER lien quan chu y chung.", "JASPER | Joint Attention, Symbolic Play, Engagement and Regulation", "medium", False, ""),
"47AB73A019": (2, "Chi muc tieu giao tiep co 'chi/tro de chia se su quan tam' - hanh vi chu y chung.", "Show or points to share interest", "medium", False, ""),
"62DDD32E72": (2, "Do luong so lan khoi xuong chu y chung truoc/sau can thiep, co so lieu cu the.", "Joint attention initiations remained constant between baseline (mean=1.67, SD=1.07) to post intervention (mean=1.67, SD=1.21) but increased at follow-up (mean=2.16, SD=1.34)", "medium", False, ""),
"0526E0659C": (1, "Chi la bang giai thich tu viet tat JASPER va IJA lien quan chu y chung.", "IJA initiation of joint attention", "medium", False, ""),
"FC8525F117": (0, "Bang tu khoa tim kiem ve tich hop cam giac, khong lien quan chu y chung.", "", "high", False, ""),
"617FCD0C69": (3, "JASPER nham cai thien chu y chung, nghien cuu cho thay hieu qua ro ret khi tap.", "JASPER aims to improve joint attention and teach play skills.", "high", False, ""),
"EA30FE8D86": (1, "Chi nhac chu y chung la mot hanh vi duoc quan sat trong danh gia tu ky.", "joint attention, restricted and repetitive behaviors, conversation", "medium", False, ""),
"D54EA1C15D": (2, "JASPER duoc khuyen nghi la can thiep huong den giao tiep xa hoi som gom chu y chung.", "joint attention, symbolic play, engagement and regulation (JASPER), which target early social communication in the context of natural interactions.", "medium", False, ""),
"D3D6A3F8E1": (2, "Huong dan cha me theo doi anh nhin cua tre va noi ve dieu tre dang chu y.", "Notice where your child\u2019s eyes are looking and what your child is doing.", "medium", False, ""),
}

assert set(labels.keys()) == set(blocks.keys()), (set(labels)-set(blocks), set(blocks)-set(labels))

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_19/q016.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for code, content in blocks.items():
        grade, rationale, span, conf, nr, note = labels[code]
        if span:
            if span not in content:
                print("MISMATCH", code)
                sys.exit(1)
        obj = {
            "annotation_code": code,
            "grade": grade,
            "rationale": rationale,
            "evidence_span": span,
            "confidence": conf,
            "needs_review": nr,
            "review_note": note,
        }
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

print("OK", len(blocks))
