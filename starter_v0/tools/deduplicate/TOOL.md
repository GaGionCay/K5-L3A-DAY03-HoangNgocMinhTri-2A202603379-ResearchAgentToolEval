---
name: deduplicate
track: core
kind: local_formatter
provider: local
requires_env: []
inputs:
- items
outputs:
- items
- input_count
- item_count
- removed_count
side_effect: false
---

# deduplicate

Loại bỏ item TRÙNG URL từ danh sách đã có, giữ item đầu tiên và thứ tự ban đầu. Dùng khi lọc trùng hoặc gộp nhiều nguồn trước format. Không tìm kiếm, đọc URL, đánh giá uy tín hay gộp các bài khác URL dù cùng nội dung.

## Khi dùng

Lọc trùng URL trong kết quả đã thu thập.

## Khi không dùng

Cần tìm kiếm, đọc nội dung, đánh giá nguồn hoặc phát hiện trùng nội dung khác URL.

## Arguments và kết quả

items là danh sách object, mỗi item có url chuỗi không rỗng. Bỏ khoảng trắng đầu/cuối khi so sánh; không tự bỏ query string hoặc đổi đường dẫn. Giữ bản ghi đầu tiên. Input sai trả invalid_input, không sửa danh sách gốc.

## Ví dụ

```python
deduplicate(items=[{'url':'https://example.com/a'},{'url':'https://example.com/a'}])
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
