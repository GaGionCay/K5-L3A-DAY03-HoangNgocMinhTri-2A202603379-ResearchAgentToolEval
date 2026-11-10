---
name: social_search
track: core
kind: live_api
provider: RapidAPI Twitter API45
requires_env:
- RAPIDAPI_KEY
- RAPIDAPI_TWITTER_HOST
inputs:
- query
- search_type
- limit
outputs:
- query
- search_type
- items
side_effect: false
---

# social_search

Tìm bài đăng trên X/Twitter THEO TỪ KHÓA. search_type=Latest cho mới nhất, Top cho nổi bật; limit từ 1 đến 100. Không dùng cho tin web hoặc bài của một tài khoản cụ thể. Nếu người dùng đã bỏ X và chuyển sang web, chỉ dùng lookup.

## Khi dùng

Tìm thảo luận hoặc bài đăng X theo một chủ đề.

## Khi không dùng

Tin web, đọc URL, hoặc lấy timeline của một tài khoản.

## Arguments và kết quả

query không rỗng. search_type phân biệt hoa thường: Top hoặc Latest. limit là số nguyên 1-100. Trả tối đa limit item có ID từ trang API đầu tiên.

## Ví dụ

```python
social_search(query='AI agents', search_type='Latest', limit=3)
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
