---
name: timeline
track: core
kind: live_api
provider: RapidAPI Twitter API45
requires_env:
- RAPIDAPI_KEY
- RAPIDAPI_TWITTER_HOST
inputs:
- screenname
- limit
outputs:
- screenname
- items
side_effect: false
---

# timeline

Lấy bài đăng mới nhất CỦA một tài khoản X/Twitter đã xác định. Dùng screenname không có @, limit từ 1 đến 100. Không dùng để tìm bài theo chủ đề; dùng social_search cho từ khóa. Nếu thiếu tài khoản, dùng clarify; không đoán.

## Khi dùng

Người dùng muốn xem bài đăng của một tài khoản cụ thể.

## Khi không dùng

Tìm từ khóa trên X, tin web, hoặc chưa biết tài khoản.

## Arguments và kết quả

screenname không có @; code cũng chấp nhận và bỏ một @ đầu chuỗi. limit là số nguyên 1-100. Trả tối đa limit bài có ID, giữ thứ tự API. Đây là trang kết quả đầu tiên, không tự phân trang.

## Ví dụ

```python
timeline(screenname='nasa', limit=3)
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
