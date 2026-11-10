---
name: send
track: bonus
kind: action
provider: Telegram Bot API
requires_env:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID
inputs:
- text
- confirmed
outputs:
- status
side_effect: true
requires_confirmation: true
---

# send

Gửi nguyên văn text tới kênh Telegram đã cấu hình. CHỈ dùng khi người dùng đã xác nhận nội dung và đích gửi; khi đó confirmed=true. Nếu chưa xác nhận, dùng clarify với response_type=yes_no. Không dùng để trả lời thông thường, soạn nháp, hoặc khi còn thiếu nội dung/đích gửi. Không tự suy diễn sự đồng ý.

## Khi dùng

Người dùng đã duyệt rõ nội dung và kênh gửi được cấu hình.

## Khi không dùng

Chưa có xác nhận, chỉ đang soạn nháp hoặc trả lời câu hỏi.

## Arguments và kết quả

confirmed phải là boolean true thực sự; chuỗi 'true', 'false' và số 1 không cấp quyền gửi. text không rỗng, tối đa 4096 ký tự. Chỉ báo sent khi HTTP thành công và Telegram trả ok=true. Bot token được che trong thông báo lỗi.

## Ví dụ

```python
send(text='Nội dung đã được duyệt', confirmed=True)
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
