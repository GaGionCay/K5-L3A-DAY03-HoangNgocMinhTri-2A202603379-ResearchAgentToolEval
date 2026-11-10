---
name: fetch
track: core
kind: live_api
provider: Firecrawl
requires_env:
- FIRECRAWL_API_KEY
inputs:
- url
outputs:
- url
- items
side_effect: false
---

# fetch

Đọc nội dung một URL HTTP(S) cụ thể bằng Firecrawl. Dùng khi người dùng đã cung cấp link bài viết. Không dùng để tìm nguồn mới hoặc khi URL còn thiếu; hãy clarify thay vì tạo URL. Trả đoạn nội dung Markdown tối đa 4000 ký tự.

## Khi dùng

Đã có URL bài viết cần đọc hoặc tóm tắt.

## Khi không dùng

Chưa có URL, chỉ có từ khóa, hoặc cần tìm kiếm trên web.

## Arguments và kết quả

url phải là URL HTTP(S) đầy đủ có hostname. summary chỉ gồm tối đa 4000 ký tự đầu, không phải toàn bộ bài dài. Tool lấy nội dung; model chịu trách nhiệm tóm tắt và dẫn nguồn.

## Ví dụ

```python
fetch(url='https://www.python.org/about/')
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
