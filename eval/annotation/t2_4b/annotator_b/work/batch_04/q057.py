from lib import run
R = [
("7E55EC48E2", 2, "Đề cập tranh cãi về vai trò của vắc-xin trẻ em trong tự kỷ, nêu nghiên cứu đề xuất đã bị rút lại; không có dữ liệu phủ nhận trực tiếp.", "alleged role of routine childhood vaccinations in autism and GI tract dysfunction, infamously suggested in a now retracted study", "medium"),
("F62A6963F1", 1, "Liệt kê các yếu tố nguy cơ của ASD (không nhắc vắc-xin), chỉ gián tiếp trả lời nguyên nhân.", "There is not just one cause of ASD.", "medium"),
("A28D4376C2", 1, "Nêu bệnh căn tự kỷ phức tạp do gen và môi trường, không nhắc vắc-xin; chỉ bối cảnh.", "the aetiology of autism to be complex, with interactive genetic and environmental factors likely contributing to markers of autism", "low"),
]
run('q057', R, default_zero="Không đề cập vắc-xin hay mối liên quan vắc-xin với tự kỷ.")
