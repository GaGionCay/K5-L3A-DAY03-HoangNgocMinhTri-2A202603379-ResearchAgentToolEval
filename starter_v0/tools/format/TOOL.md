---
name: format
track: core
kind: local_formatter
requires_env: []
inputs:
- items
- template
- headline
outputs:
- template
- markdown
- item_count
side_effect: false
---

# format

Trình bày danh sách item ĐÃ CÓ thành bản tin Markdown. Dùng sau thu thập dữ liệu. template là brief, sections, bullets, thread hoặc daily_ai_vn. Không tìm kiếm, đọc URL hay tự kiểm chứng dữ liệu. Giữ nguồn/URL từ item; không tạo nguồn mới.

## Khi dùng

Đã có kết quả cần trình bày thành bản tin hoặc thread.

## Khi không dùng

Chưa thu thập dữ liệu hoặc cần kiểm chứng nguồn.

## Arguments và kết quả

items là danh sách object; None hoặc [] trả bản tin rỗng. Item có thể thiếu url/source. brief hiển thị tối đa 5 item; item_count đếm toàn bộ đầu vào. sections nhóm theo section. summary dài được rút gọn ở 280 ký tự.

## Ví dụ

```python
format(items=[{'title':'Tin A','url':'https://example.com/a'}], template='bullets')
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
