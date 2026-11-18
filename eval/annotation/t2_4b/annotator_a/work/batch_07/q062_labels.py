from writer import parse, write
d=parse('q062')
R="Đoạn văn nói về nghiên cứu/tài liệu y khoa, không có thông tin nào về thời tiết hôm nay."
write('q062',{c:(0,R,"","high") for c in d})
