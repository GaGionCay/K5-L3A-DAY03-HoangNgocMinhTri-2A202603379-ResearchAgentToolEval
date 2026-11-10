# Hoàn thiện bộ tool

- Phạm vi: clarify, timeline, social_search, lookup, fetch, format, send, policy, papers, paper_text, deduplicate.
- Mọi tool có TOOL.md đúng tên, description về routing, khi dùng/không dùng, quy ước arguments.
- Input rỗng/sai kiểu/sai enum hoặc count không dương trả error dict. Chuỗi số nguyên dương được chuẩn hóa.
- Không đổi tên tool, không sửa eval_base.json hoặc các run JSON đã có.
- Không đọc/copy API key trong .env.
- Test: 210 passed, 0 failed, 0 skipped (175 test tool + 9 test bộ chấm + 26 test ngày giờ), toàn bộ offline.
- Bằng chứng: tools_unit_tests.txt, tools_regression_before.txt.
- Đã đo: base v5-tools-complete 19/20 (95%); group v5-evalfix 10/10 (100%). Xem REPORT Phần B cho lỗi bộ chấm và lỗi live còn lại.
- Khởi động lại Streamlit và tạo cuộc trò chuyện mới để nạp các tool đã sửa.

## Quyết định về input biên

- limit/max_results/top_k/max_pages/max_chars=0 hoặc âm trả ValueError, không ngầm dùng mặc định.
- Lookup mặc định timeframe=None để không lọc ngày xuất bản khi không được yêu cầu; max_age_hours=0 yêu cầu fetch live cho trang cập nhật liên tục.
- fetch trả tối đa 4000 ký tự đầu của Markdown, không hứa toàn bộ bài dài.
- timeline/social_search chỉ lấy trang API đầu tiên, không tự phân trang.
- paper_text là trích text bằng pypdf, không OCR; có thể rỗng với PDF scan.
- deduplicate so sánh URL sau khi trim, giữ item đầu tiên; không gộp URL khác nhau.
- send không cấp quyền từ chuỗi hoặc số; True chỉ được đặt sau xác nhận thật trong hội thoại.

## Bổ sung v6-date-context

Runtime cấp ngày giờ Việt Nam mới mỗi lượt, giữ ngày nguồn trong lookup và lưu runtime_context. Xem date_context_fix.md; chưa gán điểm eval v5 cho phiên bản này.
