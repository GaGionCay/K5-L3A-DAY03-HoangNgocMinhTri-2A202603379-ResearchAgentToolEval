---
name: send
track: bonus
kind: action
provider: Telegram Bot API
requires_env:
- TELEGRAM_BOT_TOKEN
inputs:
- text
- confirmed
- destination
outputs:
- status
- draft
- destination
side_effect: true
requires_confirmation: true
---

# send

Gửi nguyên văn text tới Telegram. Nếu destination bị bỏ trống, dùng TELEGRAM_CHAT_ID đã cấu hình. LLM gọi tool với confirmed=true vẫn không đủ quyền gửi: runtime phải hiển thị chính xác draft và destination, nhận câu trả lời xác nhận ở lượt sau, rồi cấp quyền nội bộ gắn với đúng cặp text/destination.

## Khi dùng

Chỉ gửi sau khi người dùng đã duyệt rõ draft và destination đang chờ xác nhận.

## Khi không dùng

Chưa có xác nhận, chỉ đang soạn nháp hoặc trả lời câu hỏi.

## Arguments và kết quả

confirmed phải là boolean true thực sự, nhưng tự nó không cấp quyền gửi. Quyền nội bộ phải khớp chính xác text và destination đã được hiển thị trước đó; destination phải được cung cấp hoặc có trong TELEGRAM_CHAT_ID. text không rỗng, tối đa 4096 ký tự. Chỉ báo sent khi HTTP thành công và Telegram trả ok=true. Bot token được che trong thông báo lỗi.

## Ví dụ

Thực hiện qua chat/UI: hiển thị draft và destination, chờ lượt xác nhận riêng, rồi gửi đúng draft đang chờ. Gọi tool trực tiếp với `confirmed=True` vẫn trả về `needs_confirmation`.

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
