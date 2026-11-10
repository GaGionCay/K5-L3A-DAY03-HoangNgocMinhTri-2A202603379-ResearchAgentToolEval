---
name: papers
track: bonus
kind: live_api
provider: arXiv API
requires_env:
- ARXIV_USER_AGENT
inputs:
- query
- max_results
- sort_by
outputs:
- query
- api_query
- total_results
- items
- rate_limit_note
side_effect: false
---

# papers

Tìm metadata, abstract và link paper TRÊN ARXIV theo từ khóa. Không tải toàn văn PDF; dùng paper_text sau khi biết ID. max_results từ 1 đến 10; sort_by là relevance, lastUpdatedDate hoặc submittedDate. Paper arXiv không mặc nhiên đã phản biện.

## Khi dùng

Tìm nghiên cứu, abstract và liên kết paper arXiv.

## Khi không dùng

Đã có ID cần toàn văn hoặc đang tìm tin tức thông thường.

## Arguments và kết quả

query không rỗng; có thể dùng cú pháp arXiv như ti:attention. max_results là số nguyên 1-10. Tool giới hạn tần suất trong process và thử lại tối đa 3 request khi gặp HTTP 429; lỗi API/XML trả error dict.

## Ví dụ

```python
papers(query='agent evaluation', max_results=3, sort_by='relevance')
```

## Lỗi

Input sai hoặc lỗi dịch vụ trả về `error` và `message` thay vì làm dừng agent. Test HTTP dùng mock; kết quả unit test không chứng minh API thật đã hoạt động.
