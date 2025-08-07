import os
from pypdf import PdfReader, PdfWriter

def split_pdf_in_half(input_file, output_prefix="split"):
    """
    Tách file PDF thành 2 phần bằng nhau
    
    Args:
        input_file (str): Đường dẫn tới file PDF gốc
        output_prefix (str): Tiền tố cho tên file đầu ra
    """
    try:
        # Đọc file PDF
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        print(f"File PDF có {total_pages} trang")
        
        # Tính số trang cho mỗi phần
        pages_per_part = total_pages // 2
        remaining_pages = total_pages % 2
        
        # Phần 1
        writer1 = PdfWriter()
        for i in range(pages_per_part + remaining_pages):
            writer1.add_page(reader.pages[i])
        
        output_file1 = f"{output_prefix}_part1.pdf"
        with open(output_file1, 'wb') as output1:
            writer1.write(output1)
        
        # Phần 2  
        writer2 = PdfWriter()
        for i in range(pages_per_part + remaining_pages, total_pages):
            writer2.add_page(reader.pages[i])
            
        output_file2 = f"{output_prefix}_part2.pdf"
        with open(output_file2, 'wb') as output2:
            writer2.write(output2)
        
        # Kiểm tra kích thước file
        size1 = os.path.getsize(output_file1)
        size2 = os.path.getsize(output_file2)
        original_size = os.path.getsize(input_file)
        
        print(f"File gốc: {original_size/1024:.1f} KB")
        print(f"Phần 1: {size1/1024:.1f} KB - {len(writer1.pages)} trang")
        print(f"Phần 2: {size2/1024:.1f} KB - {len(writer2.pages)} trang")
        print(f"Đã tạo: {output_file1} và {output_file2}")
        
    except Exception as e:
        print(f"Lỗi: {e}")

# Cách sử dụng
if __name__ == "__main__":
    # Thay "your_file.pdf" bằng tên file PDF của bạn
    input_pdf = "khoa-hoc-lop-5-ket-noi-tri-thuc-compressed.pdf"
    
    # Kiểm tra file có tồn tại không
    if os.path.exists(input_pdf):
        split_pdf_in_half(input_pdf, "document")
    else:
        print(f"Không tìm thấy file: {input_pdf}")

# Phiên bản nâng cao: Tách theo kích thước file
def split_pdf_by_size(input_file, target_size_kb=14):
    """
    Tách PDF dựa trên kích thước mục tiêu (tương đối)
    """
    reader = PdfReader(input_file)
    total_pages = len(reader.pages)
    original_size = os.path.getsize(input_file)
    
    # Ước tính số trang cho kích thước mục tiêu
    pages_for_target = int((target_size_kb * 1024 / original_size) * total_pages)
    
    # Phần 1
    writer1 = PdfWriter()
    for i in range(min(pages_for_target, total_pages)):
        writer1.add_page(reader.pages[i])
    
    # Phần 2
    writer2 = PdfWriter()
    for i in range(pages_for_target, total_pages):
        writer2.add_page(reader.pages[i])
    
    # Lưu file
    with open("part1_by_size.pdf", 'wb') as f1:
        writer1.write(f1)
    
    with open("part2_by_size.pdf", 'wb') as f2:
        writer2.write(f2)
    
    print(f"Đã tách dựa trên ước tính kích thước {target_size_kb}KB")
    print(f"Part 1: {os.path.getsize('part1_by_size.pdf')/1024:.1f}KB")
    print(f"Part 2: {os.path.getsize('part2_by_size.pdf')/1024:.1f}KB")