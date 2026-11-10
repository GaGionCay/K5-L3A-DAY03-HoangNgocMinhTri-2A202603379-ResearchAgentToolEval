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
outputs:
- query
- topic
- timeframe
- items
side_effect: false
---

# lookup

Tìm thông tin TRÊN WEB. Dùng topic=news cho tin tức, general cho thông tin chung. timeframe=day cho hôm nay; week, month hoặc year cho khoảng tương ứng. Giữ query tập trung vào chủ đề. Không dùng để tìm tweet hay đọc URL đã có. Nếu đổi nguồn ở lượt sau, theo nguồn mới nhất.

## Khi dùng

Tìm nguồn web hoặc tin tức theo chủ đề và thời gian.

## Khi không dùng

Tìm trên X/Twitter hoặc đọc một URL cụ thể đã biết.

## Arguments và kết quả

query không rỗng; topic là general hoặc news. timeframe là day/week/month/year; mặc định hiện tại là week. Code chấp nhận timeframe=None để bỏ time_range. max_results là số nguyên 1-20. Chuỗi số nguyên được code chuyển sang số; 0 hoặc số âm trả lỗi.

## Ví dụ

```python
lookup(query='robotics', topic='news', timeframe='day', max_results=3)
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
