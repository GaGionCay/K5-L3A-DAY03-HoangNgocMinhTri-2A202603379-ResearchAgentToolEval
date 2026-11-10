# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team:
- Members:
- Provider/model:

---

# PHẦN A — Giới thiệu agent

**Research Agent — tìm tin, đọc bài và tổng hợp bản tin**

**Bản demo hiện tại: 11 tool · 1 tool nhóm tự viết · 175 test PASS.**

## A1. Agent này làm được gì

Bạn có thể nhờ agent tìm tin trên web, theo dõi bài đăng trên X/Twitter, đọc một đường link và gom kết quả thành bản tin kèm nguồn. Agent còn có công cụ tìm paper trên arXiv, tra cứu chính sách nội bộ, lọc kết quả trùng URL và gửi bản tin qua Telegram sau khi được xác nhận.

**Mở demo:** [Research Agent](https://cooking-questions-fastest-diffs.trycloudflare.com)

Nhập yêu cầu vào ô chat; nếu agent cần bổ sung tài khoản hoặc URL, trả lời ngay ở lượt tiếp theo. Chọn **Cuộc trò chuyện mới** khi muốn bắt đầu chủ đề khác.

Link demo là link tạm thời, hoạt động khi nhóm giữ Streamlit và Cloudflare Tunnel chạy. Nếu khởi động lại tunnel, nhóm sẽ cập nhật địa chỉ mới.

## A2. Tool agent có

| Tên tool | Làm được gì | Đã hoàn thiện code, mô tả và test? |
|---|---|---|
| `clarify` | Hỏi thêm thông tin còn thiếu hoặc xin xác nhận trước khi gửi. | Có |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản X/Twitter cụ thể. | Có |
| `social_search` | Tìm bài đăng trên X/Twitter theo từ khóa, chọn bài mới nhất hoặc nổi bật. | Có |
| `lookup` | Tìm nguồn web và tin tức theo chủ đề, khoảng thời gian. | Có |
| `fetch` | Đọc nội dung từ một URL đã có để phục vụ tóm tắt. | Có |
| `format` | Trình bày dữ liệu đã thu thập thành bản tin hoặc thread Markdown. | Có |
| `send` | Gửi nội dung đã được người dùng duyệt tới kênh Telegram đã cấu hình. | Có |
| `policy` | Tìm thông tin trong kho chính sách nội bộ của bài lab. | Có |
| `papers` | Tìm paper trên arXiv, trả về abstract và liên kết nguồn. | Có |
| `paper_text` | Tải PDF arXiv và trích văn bản theo số trang, số ký tự yêu cầu. | Có |
| `deduplicate` | Loại bỏ kết quả trùng URL, giữ bản ghi đầu tiên và thứ tự ban đầu. | Có |

Tool mới của nhóm là **`deduplicate`**. Khi tổng hợp nhiều danh sách kết quả, tool giúp loại các bản ghi lặp lại trước bước trình bày bản tin; tool chạy cục bộ và không cần API key.

**Đã kiểm tra:** Bộ test offline đạt **175 PASS, 0 FAIL, 0 ERROR, 0 SKIP**, gồm contract, input hợp lệ/sai kiểu và các nhánh lỗi. Test HTTP dùng mock; khả năng gọi dịch vụ thật còn phụ thuộc API key, quyền truy cập và hạn mức. Telegram cần cấu hình bot/kênh và xác nhận của người dùng trước khi gửi.

## A3. Câu hỏi mẫu để thử

1. **Tin web:** “Tìm 5 tin tức AI trong hôm nay, kèm liên kết nguồn.”
2. **Bài đăng theo tài khoản:** “Lấy 3 bài đăng mới nhất của tài khoản sama trên X/Twitter.”
3. **Đọc bài viết:** “Đọc và tóm tắt trang https://www.python.org/about/ giúp tôi.”
4. **Tìm paper:** “Tìm 3 paper trên arXiv về agent evaluation, kèm abstract và link.”
5. **Thử tool mới:** “Lọc trùng theo URL trong danh sách dưới đây, giữ bản ghi đầu tiên. Chỉ lọc danh sách, không mở các URL.”

   ```json
   [
     {"title": "Tin A", "url": "https://example.com/a"},
     {"title": "Tin A bản sao", "url": "https://example.com/a"},
     {"title": "Tin B", "url": "https://example.com/b"}
   ]
   ```

   Kết quả mong đợi: còn 2 bản ghi là **Tin A** và **Tin B**.

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |
| Tool unit tests (`tests/`) | `pytest` output |  |  |

**Tool unit tests:** Đã thay toàn bộ 17 stub TODO bằng test có assertion và bổ sung test input biên, lỗi HTTP/timeout, arXiv và PDF. Bộ test offline sau cập nhật: **175 passed, 0 failed, 0 skipped**. Bằng chứng: `artifacts/tools_unit_tests.txt`.

Ba lỗi thực tế đã được kiểm chứng bằng regression test trên code cũ:

- `send` chấp nhận chuỗi `"false"`/`"true"` và số `1` như xác nhận. Bản sửa chỉ chấp nhận boolean `True` và kiểm tra cả trường `ok` của Telegram.
- `timeline` truyền nguyên handle có `@`/khoảng trắng và có thể mất URL khi API không trả handle. Bản sửa chuẩn hóa handle và dựng URL từ tài khoản đã biết.
- `paper_text` áp ngưỡng tối thiểu 1000 ký tự, làm sai yêu cầu `max_chars=4`. Bản sửa tôn trọng giới hạn ký tự dương được yêu cầu.

Các test hồi quy này có **5 failed, 3 passed** trên code cũ và đều PASS sau sửa. Ví dụ eval chỉ đo việc model gọi `send` với arguments nào; unit test còn phát hiện code có thực sự chặn giá trị xác nhận sai kiểu hay không.

Test HTTP dùng mock, PDF dùng dữ liệu cục bộ; không gửi Telegram hoặc gọi API thật. Chức năng live cần key, quyền truy cập và hạn mức dịch vụ hợp lệ. Điểm eval v0–v3 vẫn là bằng chứng của các phiên bản trước; chưa có điểm model eval cho bộ tool vừa cập nhật.

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?

## B7. Small Local Model Challenge (bonus)

Only fill if your team did the local model challenge.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?
