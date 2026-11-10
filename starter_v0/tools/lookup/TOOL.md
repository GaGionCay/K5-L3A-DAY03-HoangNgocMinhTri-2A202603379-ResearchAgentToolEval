---
name: lookup
track: core
kind: live_api
provider: Tavily
requires_env:
- TAVILY_API_KEY
inputs:
- query
- topic
- timeframe
- max_results
- max_age_hours
outputs:
- query
- topic
- timeframe
- max_age_hours
- retrieved_at
- items
side_effect: false
---

# lookup

Tìm nguồn web và tin tức bằng Tavily. Không tìm tweet hoặc tự tạo URL.

## Khi dùng

Tìm thông tin theo chủ đề, tin mới hoặc nguồn cập nhật liên tục như giá và thời tiết.

## Khi không dùng

Đọc URL đã có (dùng fetch), tìm trên X (dùng social_search), hoặc lấy bài theo account (dùng timeline).

## Arguments và thời gian

- query không rỗng; dùng ngày hiện tại từ runtime context cho yêu cầu “hôm nay”, không tự đoán ngày.
- topic: general hoặc news. Tin tức hôm nay dùng news và timeframe=day.
- timeframe: day/week/month/year; mặc định None nên không áp bộ lọc ngày nếu không được yêu cầu.
- max_results: số nguyên 1-20.
- max_age_hours: tùy chọn, số nguyên 0-720. 0 yêu cầu Tavily fetch trang live; 1-720 giới hạn tuổi cache. Với trang giá/thời tiết cập nhật liên tục, bỏ timeframe để không loại trang có ngày xuất bản cũ.
- published_date trong item là ước lượng ngày xuất bản/cập nhật từ Tavily, được giữ khi có. Thiếu ngày thì không tự tạo ngày.
- retrieved_at là lúc tool truy xuất, theo UTC+7. Ngày truy xuất không chứng minh con số giá trong nội dung là giá hiện tại.

## Ví dụ

```python
lookup(query="robotics", topic="news", timeframe="day", max_results=3)
lookup(query="giá vàng SJC hôm nay", topic="general", max_age_hours=0)
```

## Lỗi và giới hạn

Input sai, thiếu key hoặc lỗi HTTP trả error dict. Ngay cả fetch live cũng có thể đọc nguồn chứa số liệu cũ; agent phải kiểm tra thời điểm dữ liệu và nêu rõ nếu chưa xác minh được. Không biến ngày bài viết thành ngày hiện tại.

Tài liệu API: https://docs.tavily.com/documentation/api-reference/endpoint/search
