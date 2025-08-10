import os
from pypdf import PdfReader, PdfWriter

def split_pdf_in_three(input_file, output_prefix="split"):
    """
    Tách file PDF thành 3 phần bằng nhau
    
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
        pages_per_part = total_pages // 3
        remaining_pages = total_pages % 3
        
        # Tính chỉ số trang cho từng phần
        # Phần 1: từ 0 đến pages_per_part + (1 nếu có trang dư)
        part1_end = pages_per_part + (1 if remaining_pages > 0 else 0)
        
        # Phần 2: từ part1_end đến part1_end + pages_per_part + (1 nếu còn trang dư)
        part2_end = part1_end + pages_per_part + (1 if remaining_pages > 1 else 0)
        
        # Phần 1
        writer1 = PdfWriter()
        for i in range(part1_end):
            writer1.add_page(reader.pages[i])
        
        output_file1 = f"{output_prefix}_part1.pdf"
        with open(output_file1, 'wb') as output1:
            writer1.write(output1)
        
        # Phần 2
        writer2 = PdfWriter()
        for i in range(part1_end, part2_end):
            writer2.add_page(reader.pages[i])
            
        output_file2 = f"{output_prefix}_part2.pdf"
        with open(output_file2, 'wb') as output2:
            writer2.write(output2)
            
        # Phần 3
        writer3 = PdfWriter()
        for i in range(part2_end, total_pages):
            writer3.add_page(reader.pages[i])
            
        output_file3 = f"{output_prefix}_part3.pdf"
        with open(output_file3, 'wb') as output3:
            writer3.write(output3)
        
        # Kiểm tra kích thước file
        size1 = os.path.getsize(output_file1)
        size2 = os.path.getsize(output_file2)
        size3 = os.path.getsize(output_file3)
        original_size = os.path.getsize(input_file)
        
        print(f"File gốc: {original_size/1024:.1f} KB")
        print(f"Phần 1: {size1/1024:.1f} KB - {len(writer1.pages)} trang")
        print(f"Phần 2: {size2/1024:.1f} KB - {len(writer2.pages)} trang")
        print(f"Phần 3: {size3/1024:.1f} KB - {len(writer3.pages)} trang")
        print(f"Đã tạo: {output_file1}, {output_file2} và {output_file3}")
        
    except Exception as e:
        print(f"Lỗi: {e}")

# Cách sử dụng
if __name__ == "__main__":
    # Thay "your_file.pdf" bằng tên file PDF của bạn
    input_pdf = "thuvienhoclieu.com-SGK-Ngu-van-9-Canh-dieu-tap-1.pdf"
    
    # Kiểm tra file có tồn tại không
    if os.path.exists(input_pdf):
        split_pdf_in_three(input_pdf, "document")
    else:
        print(f"Không tìm thấy file: {input_pdf}")

# Phiên bản nâng cao: Tách theo kích thước file thành 3 phần
def split_pdf_by_size_three(input_file, target_size_kb=14):
    """
    Tách PDF thành 3 phần dựa trên kích thước mục tiêu (tương đối)
    """
    reader = PdfReader(input_file)
    total_pages = len(reader.pages)
    original_size = os.path.getsize(input_file)
    
    # Ước tính số trang cho kích thước mục tiêu (mỗi phần)
    pages_for_target = int((target_size_kb * 1024 / original_size) * total_pages)
    
    # Đảm bảo không vượt quá tổng số trang
    if pages_for_target > total_pages // 3:
        pages_for_target = total_pages // 3
    
    # Phần 1
    writer1 = PdfWriter()
    for i in range(min(pages_for_target, total_pages)):
        writer1.add_page(reader.pages[i])
    
    # Phần 2
    writer2 = PdfWriter()
    start_page2 = pages_for_target
    end_page2 = min(pages_for_target * 2, total_pages)
    for i in range(start_page2, end_page2):
        writer2.add_page(reader.pages[i])
    
    # Phần 3
    writer3 = PdfWriter()
    for i in range(end_page2, total_pages):
        writer3.add_page(reader.pages[i])
    
    # Lưu file
    with open("part1_by_size.pdf", 'wb') as f1:
        writer1.write(f1)
    
    with open("part2_by_size.pdf", 'wb') as f2:
        writer2.write(f2)
        
    with open("part3_by_size.pdf", 'wb') as f3:
        writer3.write(f3)
    
    print(f"Đã tách thành 3 phần dựa trên ước tính kích thước {target_size_kb}KB mỗi phần")
    print(f"Part 1: {os.path.getsize('part1_by_size.pdf')/1024:.1f}KB - {len(writer1.pages)} trang")
    print(f"Part 2: {os.path.getsize('part2_by_size.pdf')/1024:.1f}KB - {len(writer2.pages)} trang")
    print(f"Part 3: {os.path.getsize('part3_by_size.pdf')/1024:.1f}KB - {len(writer3.pages)} trang")

# Hàm linh hoạt: Tách PDF thành N phần
def split_pdf_into_n_parts(input_file, n_parts=3, output_prefix="split"):
    """
    Tách file PDF thành N phần bằng nhau
    
    Args:
        input_file (str): Đường dẫn tới file PDF gốc
        n_parts (int): Số phần muốn tách
        output_prefix (str): Tiền tố cho tên file đầu ra
    """
    try:
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        
        print(f"File PDF có {total_pages} trang, tách thành {n_parts} phần")
        
        pages_per_part = total_pages // n_parts
        remaining_pages = total_pages % n_parts
        
        current_page = 0
        output_files = []
        
        for part in range(n_parts):
            writer = PdfWriter()
            
            # Số trang cho phần này
            pages_in_this_part = pages_per_part + (1 if part < remaining_pages else 0)
            
            # Thêm trang vào phần này
            for i in range(current_page, current_page + pages_in_this_part):
                if i < total_pages:
                    writer.add_page(reader.pages[i])
            
            # Lưu file
            output_file = f"{output_prefix}_part{part + 1}.pdf"
            with open(output_file, 'wb') as output:
                writer.write(output)
            
            output_files.append(output_file)
            
            # In thông tin
            size = os.path.getsize(output_file)
            print(f"Phần {part + 1}: {size/1024:.1f} KB - {len(writer.pages)} trang")
            
            current_page += pages_in_this_part
        
        print(f"Đã tạo: {', '.join(output_files)}")
        
    except Exception as e:
        print(f"Lỗi: {e}")