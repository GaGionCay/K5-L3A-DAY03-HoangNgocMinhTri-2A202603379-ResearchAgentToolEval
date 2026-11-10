---
name: clarify
track: core
kind: control
requires_env: []
inputs:
- question
- response_type
- options
outputs:
- question
- response_type
- options
- awaiting_user
side_effect: false
---

# clarify

Hỏi người dùng và chờ lượt tiếp theo khi thiếu thông tin thiết yếu hoặc cần xác nhận. Dùng response_type=text để hỏi tài khoản/URL; yes_no để xác nhận gửi; choice cho lựa chọn. Không dùng khi thông tin đã có trong hội thoại. Không tìm kiếm hoặc gửi nội dung.

## Khi dùng

Thiếu tài khoản/URL hoặc cần xác nhận trước hành động.

## Khi không dùng

Thông tin đã rõ hoặc đã được cung cấp ở lượt trước.

## Arguments và kết quả

question phải là câu hỏi không rỗng. response_type là text, yes_no hoặc choice. choice cần ít nhất hai options không rỗng. Kết quả awaiting_user=true để dừng vòng gọi tool.

## Ví dụ

```python
clarify(question='Bạn muốn xem tài khoản nào?', response_type='text')
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
