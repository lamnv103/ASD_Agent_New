import json, re, sys

src = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/work/batch_19/q001.txt"
with open(src, "r", encoding="utf-8") as f:
    text = f.read()

# split into candidate blocks
parts = text.split("\n### ")
blocks = {}
for p in parts[1:]:
    code = p[:10]
    rest = p[len(code):]
    # content is after the header line (first newline) up to end of block
    nl = rest.find("\n")
    header = rest[:nl]
    content = rest[nl:].strip()
    blocks[code] = content

labels = {
"92EB809AA2": (0, "Noi ve ty le bo tron (elopement) va phan loai DD/ID, khong dinh nghia tu ky.", "", "high", False, ""),
"7910CB418C": (3, "Dinh nghia truc tiep ASD la roi loan phat trien than kinh voi khiem khuyet giao tiep xa hoi, hanh vi lap lai.", "Autism Spectrum Disorder (ASD) is a neurodevelopmental disorder characterized by persistent deficits in social communication and social interaction across multiple contexts and restricted, repetitive patterns of stereotyped behaviors, interests, or activities.", "high", False, ""),
"4D89F1B35C": (0, "Chi noi ve ty le hien mac ASD o Viet Nam, khong dinh nghia.", "", "high", False, ""),
"FE03034262": (3, "Dinh nghia truc tiep: ASD la khuyet tat phat trien gay kho khan xa hoi, giao tiep, hanh vi.", "Autism spectrum disorder (ASD) is a developmental disability that can cause significant social, communication, and behavioral challenges.", "high", False, ""),
"52CE14C7DE": (0, "So sanh roi loan tam than kem theo ASD va ADHD, khong dinh nghia ASD.", "", "high", False, ""),
"EEA5F5C829": (0, "Noi ve tic, Tourette di kem ASD, khong dinh nghia ASD.", "", "high", False, ""),
"4F2AE0B3B3": (3, "Dinh nghia ASD la roi loan hanh vi than kinh voi khiem khuyet giao tiep xa hoi va hanh vi lap lai.", "Autism spectrum disorder (ASD) is a neurobehavioral disorder defined by social- communication deficits and restricted and repetitive behaviors", "high", False, ""),
"882B21A1ED": (0, "Noi ve cong cu KID-SCID danh gia roi loan tam than, khong dinh nghia ASD.", "", "high", False, ""),
"561429BE6C": (3, "Dinh nghia ASD la roi loan phat trien lan toa anh huong xa hoi, hanh vi lap lai, giao tiep.", "refers to a pervasive developmental disorder that hinders an individual\u2019s skills in socialisation, creates repetitive behaviours, and impacts expressive or verbal communication with disruptions ranging from moderate to severe", "high", False, ""),
"D3D0E15949": (0, "Bang so lieu hanh vi lap lai, khong co dinh nghia.", "", "high", False, ""),
"04030C998C": (3, "Dinh nghia ASD: khiem khuyet hanh vi xa hoi, giao tiep, ngon ngu, so thich hep.", "ASDs are characterized by \u2018impaired social behavior, communication and language, and a narrow range of interests and activities that are both unique to the individual and carried out repetitively\u2019", "high", False, ""),
"8E33BC7068": (0, "Noi ve phuong phap thong ke CSBQ va bo tron, khong dinh nghia ASD.", "", "high", False, ""),
"094E70CBD6": (0, "Noi ve roi loan van dong di kem ASD, khong dinh nghia ASD noi chung.", "", "high", False, ""),
"F53FF94CEE": (0, "Noi ve ty le lo au di kem ASD, khong dinh nghia ASD.", "", "high", False, ""),
"E6EEBCBFFB": (0, "Noi ve lo au xa hoi trong ASD, khong dinh nghia ASD.", "", "high", False, ""),
"16A77EAB69": (0, "Bang tong hop nghien cuu ve lo au va ADHD, khong dinh nghia ASD.", "", "high", False, ""),
"CF8D1A1B36": (0, "Noi ve cac chuong trinh nghien cuu NIH ve ASD, khong dinh nghia.", "", "high", False, ""),
"241ABCE3AE": (0, "Bang nghien cuu ve giac ngu va hanh vi, khong dinh nghia ASD.", "", "high", False, ""),
"7E57314E11": (0, "Thao luan ve lo au va benh tam than kem theo, khong dinh nghia ASD.", "", "high", False, ""),
"4295CD3BBD": (0, "Chi la cau dan nguon tham khao them, khong co noi dung dinh nghia.", "", "high", False, ""),
"DA963FBB0B": (3, "Dinh nghia tu ky la khuyet tat phat trien voi giao tiep xa hoi, so thich hep, hanh vi lap lai.", "Autism is a neurodevelopmental disability (NDD) characterized by core features such as social communication challenges, focused interests, and repetitive behaviors", "high", False, ""),
"17F49D0CC0": (1, "Chi noi NDD la nhom benh bat dau tu thoi ky phat trien, lien quan gian tiep den tu ky.", "NDDs are a group of conditions with onset in the developmental period, and they frequently co-occur with autism.", "medium", False, ""),
"7E1041351A": (0, "Chi neu ty le benh tam than kem theo, khong dinh nghia ASD.", "", "high", False, ""),
"0B9B1CB44B": (3, "Dinh nghia truc tiep ASD la roi loan than kinh va phat trien anh huong giao tiep, hanh vi.", "Autism spectrum disorder (ASD) is a neurological and developmental disorder that affects how people interact with others, communicate, learn, and behave.", "high", False, ""),
"F9F8690B07": (0, "Noi ve ty le cac roi loan tam than kem theo ASD, khong dinh nghia.", "", "high", False, ""),
"44D5045DAD": (2, "Mot phan tieu chuan chan doan DSM-5 ve hanh vi lap lai, ho tro mot phan dinh nghia.", "Stereotyped or repetitive motor movements, use of objects, or speech (e.g., simple motor stereotypes, lining up toys or flipping objects, echolalia, idiosyncratic phrases).", "medium", False, ""),
"C38E6203D3": (3, "Dinh nghia truc tiep ASD la roi loan phat trien than kinh voi kho khan giao tiep va hanh vi lap lai.", "Autism Spectrum Disorder (ASD) is a neurodevelopmental condition characterized by challenges in social interaction and communication and the presence of restricted interests and repetitive behaviors.", "high", False, ""),
"3E254740BE": (0, "Noi ve trieu chung tieu hoa va vi sinh duong ruot, khong dinh nghia ASD.", "", "high", False, ""),
"F33CC5A084": (3, "Dinh nghia ASD: pham vi dieu kien voi khiem khuyet hanh vi xa hoi, giao tiep, so thich hep.", "Autism spectrum disorders (ASD) refer to a range of conditions characterized by some degree of impaired social behavior, communication and language, and a narrow range of interests and activities that are both unique to the individual and carried out repetitively", "high", False, ""),
"3A630D6719": (0, "Thao luan trieu chung tieu hoa lien quan ASD, khong dinh nghia ASD.", "", "high", False, ""),
"91DA6446D5": (0, "Noi ve ky thi van hoa Viet Nam voi tu ky, khong dinh nghia tu ky.", "", "medium", False, ""),
"C44A8D6522": (3, "Dinh nghia ASD la roi loan phat trien than kinh voi khiem khuyet giao tiep va hanh vi lap lai.", "Autism spectrum disorder (ASD) is a neurodevelopmental disorder characterized by impairments in social interaction and communication as well as a repetitive and/or restricted range of behaviors and interests.", "high", False, ""),
"95ACDB1A7C": (0, "Thao luan ty le OCD kem theo ASD, khong dinh nghia ASD.", "", "high", False, ""),
"532F387516": (2, "Mo ta vi du hanh vi/so thich han che o ASD, ho tro mot phan dinh nghia.", "People with ASD have behaviors or interests that can seem unusual.", "medium", False, ""),
"6DF8789650": (0, "Noi ve dinh duong va chon thuc an o tre ASD, khong dinh nghia ASD.", "", "high", False, ""),
"1FAD0E495A": (0, "Noi ve ty le ADHD, lo au kem theo ASD, khong dinh nghia ASD.", "", "high", False, ""),
"2071D9613C": (0, "Noi ve di ung thuc an va benh tieu hoa kem ASD, khong dinh nghia.", "", "high", False, ""),
}

assert set(labels.keys()) == set(blocks.keys()), (set(labels)-set(blocks), set(blocks)-set(labels))

out_path = r"D:/AI4LIFE/ASD_AGENT_FINALL/eval/annotation/t2_4b/annotator_b/returned/batch_19/q001.jsonl"
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
