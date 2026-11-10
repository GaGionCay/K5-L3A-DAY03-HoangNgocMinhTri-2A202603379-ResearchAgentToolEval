# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: HoangNgocMinhTri - 2A202603379
- Members: (Sẽ bổ sung sau)
- Provider/model: OpenRouter / openai/gpt-4o-mini

---

# PHẦN A — Giới thiệu agent

**Research Agent — tìm tin, đọc bài và tổng hợp bản tin**

**Bản demo hiện tại: 11 tool · 1 tool nhóm tự viết · 184 test PASS.**

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

**Đã kiểm tra:** Bộ test offline đạt **184 PASS, 0 FAIL, 0 ERROR, 0 SKIP**, gồm contract, input hợp lệ/sai kiểu và các nhánh lỗi. Test HTTP dùng mock; khả năng gọi dịch vụ thật còn phụ thuộc API key, quyền truy cập và hạn mức. Telegram cần cấu hình bot/kênh và xác nhận của người dùng trước khi gửi.

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

Số liệu dưới đây lấy từ run JSON và `version_log.csv`. Provider/model dùng cho các run: **OpenRouter / openai/gpt-4o-mini**.

| Version | Suite | Thay đổi | Giả thuyết / mục đích | Trước | Sau | Bằng chứng |
|---|---|---|---|---|---|---|
| v0 | base | baseline | Đo hành vi starter trước khi sửa | N/A | 14/20 case đo được (70%) | [v0_B_base_openrouter_20261110T111422879374.json](../runs/v0_B_base_openrouter_20261110T111422879374.json) |
| v1 | base | system_prompt.md | Hỏi lại thay vì đoán khi thiếu tài khoản/URL | 70% | 18/20 case đo được (90%) | [v1_B_base_openrouter_20261110T112012333650.json](../runs/v1_B_base_openrouter_20261110T112012333650.json) |
| v2 | base | system_prompt.md | Thử quy tắc xác nhận; thực tế thay nhầm đoạn hỏi thông tin | 90% | 18/20 case đo được (90%) | [v2_B_base_openrouter_20261110T112907549500.json](../runs/v2_B_base_openrouter_20261110T112907549500.json) |
| v2-fix | base | system_prompt.md | Khôi phục hỏi thông tin và bỏ chỉ dẫn gửi ngay | 90% | 16/20 case đo được (80%) | [v2-fix_B_base_openrouter_20261110T113230768428.json](../runs/v2-fix_B_base_openrouter_20261110T113230768428.json) |
| v3 | base | system_prompt.md | Làm rõ nguồn web/X và ngữ cảnh lượt sau | 80% | 18/20 case đo được (90%) | [v3_B_base_openrouter_20261110T113603331961.json](../runs/v3_B_base_openrouter_20261110T113603331961.json) |
| v5-tools-complete | base | tools.yaml; tools/; tests/ | Hoàn thiện mô tả, validation và tool mới; thay đổi gộp, không cô lập từng yếu tố | 90% | 19/20 case đo được (95%) | [v5-tools-complete_B_base_openrouter_20261110T122338476859.json](../runs/v5-tools-complete_B_base_openrouter_20261110T122338476859.json) |
| v5-tools-complete | group | Bộ group lần đầu | Đo 10 case nhóm; phát hiện lỗi comparator ở G01 | N/A — bộ group mới | 9/9 case đo được (100%); 1 case không đo được | [v5-tools-complete_B_group_openrouter_20261110T143816074250.json](../runs/v5-tools-complete_B_group_openrouter_20261110T143816074250.json) |
| v5-evalfix | group | run_eval.py; test_eval_structured_args.py | Chấm danh sách object không bị TypeError | 9/10 case đo được; 1 lỗi bộ chấm | 10/10 case đo được (100%) | [v5-evalfix_B_group_openrouter_20261110T144452606199.json](../runs/v5-evalfix_B_group_openrouter_20261110T144452606199.json) |

| Bản đo | Case PASS | Routing | Arguments | Multi turn | Case không đo được |
|---|---|---|---|---|---|
| Base — v5-tools-complete | 19/20 | 100% | 95% | 100% | 0 |
| Group — v5-evalfix | 10/10 | 100% | 100% | 100% | 0 |

Base và group là hai bộ dữ liệu khác nhau. Lần group đầu in accuracy 100% nhưng chỉ đo được 9 case; G01 bị ghi nhãn `provider_error` do lỗi bộ chấm cục bộ, không phải bằng chứng API bị lỗi. Sau khi sửa comparator, chạy lại mới có đủ 10/10 PASS. Không sửa nội dung case để làm tăng điểm.

Các version v0–v3 giữ nguyên tool declaration; v5 thay đổi cả description, validation và thêm tool. Vì nhiều yếu tố đổi cùng lúc ở v5, kết quả 95% không xác định được riêng yếu tố nào đóng góp bao nhiêu. `artifact_version` lưu hash prompt/tools.yaml; khi tái lập cần đối chiếu cả code tool và bộ chấm trong repo.

## B2. Failure Analysis

Các FAIL của eval được giữ nguyên trong log; phần nhận xét dưới đây phân biệt lỗi model với lỗi bộ chấm.

| Version/suite | Case | Nhãn lỗi | Lỗi quan sát | Tool call thực tế | Phân tích / xử lý |
|---|---|---|---|---|---|
| v0/base | R08_out_of_scope | out_of_scope | unexpected_tool_call | `send({"text":"Nguyên hàm của x^2 là \\( \\frac{x^3}{3} + C \\), trong đó \\( C \\) là hằng số tùy ý."})` | Gọi tool cho câu ngoài phạm vi. Các run sau PASS; chưa có thí nghiệm riêng để tách tác động của quy tắc phạm vi. |
| v0/base | R10_missing_handle | missing_info | missing_tool_call | `timeline({"screenname":"sama"})` | Suy diễn dữ liệu còn thiếu. v1 bổ sung hỏi lại; v2 thay nhầm đoạn và gây hồi quy; bản cuối PASS trên base nhưng còn lỗi cùng loại trong live chat. |
| v0/base | R11_missing_url | missing_info | missing_tool_call | `fetch({"url":"https://example.com/article"})` | Suy diễn dữ liệu còn thiếu. v1 bổ sung hỏi lại; v2 thay nhầm đoạn và gây hồi quy; bản cuối PASS trên base nhưng còn lỗi cùng loại trong live chat. |
| v0/base | R12_confirm_before_send | wrong_boundary | missing_tool_call | `send({"text":"Bản tin này đã được đăng lên Telegram."})` | Model chọn send trước khi xác nhận; cần hỏi clarify(yes_no). Không suy ra có tin nhắn gửi thật chỉ từ tool call. |
| v0/base | R13_parallel_web_and_tweets | wrong_tool | wrong_arg_value | `lookup({"query":"AI news","timeframe":"day","max_results":5})`; `social_search({"query":"AI","search_type":"Latest","limit":5})` | Kiểm tra observed_mismatch: lỗi ở query/topic dù nhãn case là wrong_tool. Rule routing và convention news được làm rõ; bản cuối PASS. |
| v0/base | R14_out_of_scope_coding | out_of_scope | unexpected_tool_call | `send({"text":"Dưới đây là một hàm Python tính số Fibonacci bằng đệ quy:\n\n```python\ndef fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n     ...)` | Gọi tool cho câu ngoài phạm vi. Các run sau PASS; chưa có thí nghiệm riêng để tách tác động của quy tắc phạm vi. |
| v1/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung bản tin mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi nội dung bằng clarify(text), khác kỳ vọng yes_no. Cần đánh giá thủ công vì request chưa đưa nội dung bản tin; log không cho thấy gửi ngay. |
| v1/base | M02_carryover_timeframe | wrong_arg_value | missing_tool_call | `social_search({"query":"robotics","search_type":"Latest","limit":5})` | Chọn social_search cho tin web. Cần giữ nguồn và thời gian từ ngữ cảnh; base bản cuối PASS. |
| v2/base | R10_missing_handle | missing_info | missing_tool_call | `timeline({"screenname":"twitter","limit":5})` | Suy diễn dữ liệu còn thiếu. v1 bổ sung hỏi lại; v2 thay nhầm đoạn và gây hồi quy; bản cuối PASS trên base nhưng còn lỗi cùng loại trong live chat. |
| v2/base | R11_missing_url | missing_info | missing_tool_call | `fetch({"url":"https://"})` | Suy diễn dữ liệu còn thiếu. v1 bổ sung hỏi lại; v2 thay nhầm đoạn và gây hồi quy; bản cuối PASS trên base nhưng còn lỗi cùng loại trong live chat. |
| v2-fix/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi nội dung bằng clarify(text), khác kỳ vọng yes_no. Cần đánh giá thủ công vì request chưa đưa nội dung bản tin; log không cho thấy gửi ngay. |
| v2-fix/base | R13_parallel_web_and_tweets | wrong_tool | wrong_arg_value | `lookup({"query":"AI","timeframe":"day","max_results":5})`; `social_search({"query":"AI","limit":5})` | Kiểm tra observed_mismatch: lỗi ở query/topic dù nhãn case là wrong_tool. Rule routing và convention news được làm rõ; bản cuối PASS. |
| v2-fix/base | M02_carryover_timeframe | wrong_arg_value | missing_tool_call | `social_search({"query":"robotics","search_type":"Latest","limit":5})` | Chọn social_search cho tin web. Cần giữ nguồn và thời gian từ ngữ cảnh; base bản cuối PASS. |
| v2-fix/base | M06_switch_tool | wrong_tool | missing_tool_call | `social_search({"query":"OpenAI","search_type":"Latest","limit":5})` | Không bỏ nguồn X khi người dùng đã chuyển sang web, có lúc gọi thêm social_search. Bản base cuối và G09 group đã PASS. |
| v3/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi nội dung bằng clarify(text), khác kỳ vọng yes_no. Cần đánh giá thủ công vì request chưa đưa nội dung bản tin; log không cho thấy gửi ngay. |
| v3/base | M06_switch_tool | wrong_tool | extra_tool_call | `lookup({"query":"OpenAI","topic":"news","timeframe":"day","max_results":5})`; `social_search({"query":"OpenAI","search_type":"Latest","limit":5})` | Không bỏ nguồn X khi người dùng đã chuyển sang web, có lúc gọi thêm social_search. Bản base cuối và G09 group đã PASS. |
| v5-tools-complete/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi nội dung bằng clarify(text), khác kỳ vọng yes_no. Cần đánh giá thủ công vì request chưa đưa nội dung bản tin; log không cho thấy gửi ngay. |
| v5-tools-complete/group | G01_deduplicate_items | provider_error | provider_error | Không có tool call được lưu | normalize_value dùng sorted trên list[dict], phát sinh TypeError và bị bắt nhầm là provider_error. Đã sửa, thêm 9 test và chạy lại group 10/10. |
| Live CLI | Lượt 2 | missing_info — đánh giá thủ công | Tự suy diễn account | `timeline({"screenname":"robotics","limit":2})` | Chủ đề robotics ở lượt trước không phải tài khoản được người dùng chỉ định. Cần clarify hỏi tài khoản; đây là lỗi chưa được sửa trong phiên bản hiện tại. |

## B3. Team Eval Cases

Bộ group có **10 case: 5 single turn và 5 multi turn**. Kết quả bên dưới lấy từ [v5-evalfix_B_group_openrouter_20261110T144452606199.json](../runs/v5-evalfix_B_group_openrouter_20261110T144452606199.json).

| Case ID | Loại | Nội dung kiểm tra | Tool/hành vi mong đợi | Kết quả |
|---|---|---|---|---|
| G01_deduplicate_items | Single turn | Chọn tool mới và truyền đủ danh sách gốc để tool lọc trùng. | `deduplicate({"items":"3 bản ghi đầu vào"})` | PASS |
| G02_web_news_week | Single turn | Truyền đúng chủ đề tin tức, khoảng thời gian và số kết quả. | `lookup({"query":"robotics","topic":"news","timeframe":"week","max_results":3})` | PASS |
| G03_read_given_url | Single turn | Dùng fetch khi người dùng đã cung cấp URL cụ thể. | `fetch({"url":"https://www.python.org/about/"})` | PASS |
| G04_missing_account | Single turn | Hỏi tài khoản khi chưa có thông tin trong hội thoại. | `clarify({"response_type":"text"})` | PASS |
| G05_capability_no_tool | Single turn | Giới thiệu khả năng mà không gọi tool thừa. | Không gọi tool | PASS |
| G06_fill_account | Multi turn | Ghép tài khoản vừa bổ sung với số lượng từ lượt trước. | `timeline({"screenname":"nasa","limit":2})` | PASS |
| G07_correct_limit | Multi turn | Ưu tiên số lượng được sửa ở lượt mới nhất. | `timeline({"screenname":"github","limit":2})` | PASS |
| G08_preserve_timeframe | Multi turn | Đổi chủ đề nhưng giữ loại nguồn và khoảng thời gian. | `lookup({"query":"quantum computing","topic":"news","timeframe":"week"})` | PASS |
| G09_switch_to_web | Multi turn | Chuyển sang lookup và không gọi thêm social_search. | `lookup({"query":"cybersecurity","topic":"news","timeframe":"day"})` | PASS |
| G10_confirm_known_content | Multi turn | Hỏi xác nhận khi đã có nội dung và đích gửi; chưa được gọi send. | `clarify({"response_type":"yes_no"})` | PASS |

G01 kiểm tra model chọn `deduplicate` và truyền đủ danh sách gốc; unit test riêng kiểm tra code có loại đúng bản ghi trùng hay không. G10 có đủ nội dung và đích gửi, giúp kiểm tra xác nhận rõ hơn R12 trong base. Group chưa có case phân biệt chủ đề vừa tìm trên web với handle X ở lượt sau; lỗi này được phát hiện trong live chat.

## B4. Live Chat Evidence

Transcript CLI: [v5-evalfix_openrouter_20261110T144638732811.transcript.json](../transcripts/v5-evalfix_openrouter_20261110T144638732811.transcript.json). Artifact: `v5-evalfix+pcf82e7a93a6b+t1dfc05a44ef2`. Có đủ **3 lượt live**; `/exit` kết thúc phiên.

| Lượt | Yêu cầu | Tool call thực tế | Trạng thái chạy | Đánh giá thủ công |
|---|---|---|---|---|
| 1 | Tìm 3 tin tức về robotics trên web trong tuần này, kèm nguồn. | `lookup({"query":"robotics","topic":"news","timeframe":"week","max_results":3})` | answered | Đúng tool và args: lookup(news, week, 3); tool trả 3 item, câu trả lời có nguồn. Chưa kiểm chứng thủ công từng bài gốc. |
| 2 | Lấy 2 bài đăng mới nhất trên X giúp tôi. | `timeline({"screenname":"robotics","limit":2})` | answered | CHƯA ĐÚNG: tự chọn account robotics từ chủ đề trước. Mong đợi hỏi người dùng tài khoản nào. Tool trả dữ liệu thành công không đồng nghĩa hiểu đúng yêu cầu. |
| 3 | Tài khoản nasa. | `timeline({"screenname":"nasa","limit":2})` | answered | Đúng sửa account sang nasa và giữ limit=2; tool trả 2 item. Đây là lượt người dùng sửa thông tin, không phải bằng chứng agent đã hỏi lại đúng ở lượt 2. |

`status=answered` chỉ cho biết vòng chat đã trả lời, không phải điểm PASS về chất lượng. Trong phiên này agent trả lời bằng tiếng Anh dù người dùng hỏi tiếng Việt; đây là điểm cần cải thiện cho trải nghiệm demo.

## B5. Tool, UI và kiểm thử bổ sung

| Hạng mục | Bằng chứng | Kết quả và giới hạn |
|---|---|---|
| Tool mới deduplicate | tools/deduplicate/; G01; tests/test_tools_todo.py | Đã có implementation, TOOL.md, registry và schema; G01 PASS. Lọc theo URL, không phát hiện trùng nội dung khác URL. |
| Telegram send | tests/test_tool_validation.py; tests/test_tools_todo.py; G10 | Guardrail và gửi HTTP bằng mock PASS; G10 hỏi xác nhận PASS. Chưa có bằng chứng gửi Telegram thật trong bộ transcript CLI này. |
| arXiv / policy | tests/test_tool_validation.py; tests/test_tools_todo.py | Test metadata, retry 429, PDF cục bộ và trust boundary PASS. Không dùng test mock để khẳng định mọi API live hoạt động. |
| UI | app.py; transcripts/ui_v3_*.transcript.json; link ở Phần A | Đã có UI và transcript theo phiên. Link tunnel tạm, phụ thuộc máy và hai tiến trình còn chạy. |
| Test offline | tests/; artifacts/tools_unit_tests.txt | 184 PASS, 0 FAIL, 0 ERROR, 0 SKIP: 175 test trước đó và 9 test mới cho bộ chấm. |
| Sửa bộ chấm eval | run_eval.py; tests/test_eval_structured_args.py; hai group run JSON | Giữ so sánh scalar list không phụ thuộc thứ tự; list object/nested list giữ thứ tự. Không đổi dữ liệu eval để né lỗi. |

Đã thay toàn bộ 17 stub TODO bằng test có assertion. Các lời gọi HTTP trong unit test được mock, không tiêu credit và không gửi Telegram thật. Năm test PDF dùng thư mục tạm riêng để tránh lỗi quyền truy cập `pytest-of-Admin` trên Windows.

Các lỗi tool có regression test:

- `send` từng chấp nhận chuỗi `"false"`, `"true"` và số `1` như xác nhận. Bản sửa chỉ chấp nhận boolean `True`, kiểm tra `ok=true` của Telegram và che token trong lỗi.
- `timeline` từng truyền nguyên handle có khoảng trắng/@ và có thể thiếu URL khi API không trả handle. Bản sửa chuẩn hóa handle và dựng URL từ account đã biết.
- `paper_text` từng áp tối thiểu 1000 ký tự, làm sai yêu cầu `max_chars=4`. Bản sửa tôn trọng giới hạn dương.

Nhóm test chọn để kiểm tra ba lỗi trên có **5 FAIL, 3 PASS trên code cũ**, rồi PASS sau sửa; log trước sửa: `artifacts/tools_regression_before.txt`. Sau đó bổ sung 9 test bộ chấm: trước sửa **8 FAIL, 1 PASS**, sau sửa cả 9 PASS; test CLI offline còn xác nhận `deduplicate` thực thi và tạo run có measured_cases=1 thay vì provider_error.

Ví dụ khác biệt giữa hai lớp kiểm tra: model eval có thể thấy đúng tên `send` và args; unit test mới xác minh chuỗi `"false"` thực sự không được phép đi qua nhánh gửi. Tương tự, tool deduplicate đã qua unit test nhưng scorer cũ vẫn làm G01 lỗi do không chấm được danh sách object.

## B6. Reflection

- **Thay đổi trong prompt:** hỏi thông tin còn thiếu, xác nhận trước gửi, chọn nguồn và áp dụng sửa đổi ở lượt sau. Vòng v2 thay nhầm đoạn đã gây hồi quy, cho thấy cần lưu snapshot và kiểm tra diff trước mỗi run.
- **Thay đổi trong tools.yaml:** mô tả rõ khi dùng/không dùng, phân biệt tài khoản với chủ đề, topic=news, timeframe, search_type và giới hạn tham số. Validation trong code hỗ trợ input sai từ model; description không thay thế validation.
- **Trường hợp cần đánh giá thủ công:** R12 thiếu nội dung nhưng đáp án chỉ chấp nhận yes_no; local TypeError bị log thành provider_error; live status=answered vẫn có thể chọn sai account. Không ghi những trường hợp này thành thành công chỉ vì tool trả dữ liệu.
- **Giới hạn của kết quả:** base và group là tập nhỏ, group do nhóm thiết kế và một số query gọi tên tool rõ ràng. Điểm group 100% không chứng minh độ tin cậy chung. Phiên live đã bộc lộ lỗi chuyển chủ đề thành handle mà bộ group hiện tại chưa kiểm tra.
- **Ưu tiên tiếp theo:** thêm regression case cho chuỗi “tin robotics trên web → lấy bài trên X nhưng chưa nêu account”, rồi kiểm chứng quy tắc không suy diễn topic thành handle ở một version mới. Bổ sung quy tắc trả lời cùng ngôn ngữ người dùng. Đây là việc đề xuất tiếp, chưa ghi nhận đã sửa hoặc đã có điểm mới.
- **Tái lập và nộp bài:** giữ log lỗi lẫn log thành công, đối chiếu hash prompt/tools và code scorer; che chuỗi nhạy cảm trước khi push. Bản báo cáo này không thực hiện commit/push thay người dùng.

## B7. Small Local Model Challenge (bonus)

Chưa có run Ollama trong tập bằng chứng hiện tại. Không yêu cầu điểm cho bonus local model; không tạo số liệu so sánh cloud/local khi chưa chạy.
