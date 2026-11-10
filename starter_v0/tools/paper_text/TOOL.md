---
name: paper_text
track: bonus
kind: live_api_plus_local_extract
provider: arXiv + pypdf
requires_env:
- ARXIV_USER_AGENT
inputs:
- arxiv_url
- max_pages
- max_chars
outputs:
- arxiv_id
- url
- pdf_url
- pdf_path
- txt_path
- page_count
- pages_read
- chars_returned
- items
side_effect: local_file_write
---

# paper_text

Tải PDF và trích văn bản khi ĐÃ CÓ arXiv ID hoặc URL abstract/PDF arxiv.org. Không tìm paper theo từ khóa; dùng papers trước. max_pages từ 1 đến 100, max_chars từ 1 đến 20000. Tạo file PDF/TXT cục bộ; không OCR trang scan.

## Khi dùng

Đã xác định paper arXiv và cần đọc một phần toàn văn.

## Khi không dùng

Chỉ có chủ đề tìm kiếm, URL không thuộc arXiv hoặc PDF scan cần OCR.

## Arguments và kết quả

arxiv_url nhận ID mới/legacy và URL arxiv.org/abs hoặc /pdf. max_pages và max_chars là giới hạn dương. pages_read không vượt số trang PDF. PDF/TXT được ghi trong arxiv_papers; PDF scan có thể không trích được chữ.

## Ví dụ

```python
paper_text(arxiv_url='1706.03762', max_pages=2, max_chars=4000)
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
