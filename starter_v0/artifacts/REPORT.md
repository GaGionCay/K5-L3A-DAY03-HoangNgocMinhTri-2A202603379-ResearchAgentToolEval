# Báo cáo Day 03 — Research Agent

Báo cáo gồm hai phần: Phần A giới thiệu agent và cách dùng thử; Phần B ghi lại quá trình cải thiện, kết quả kiểm thử và những vấn đề còn cần xử lý. Các nhận xét trong báo cáo đều dựa trên run JSON, transcript hoặc kiểm tra code được lưu trong repo.

## Thông tin nhóm

- Team: HoangNgocMinhTri-2A202603379
- Thành viên: 
  + Nguyễn Thế Cường - 2A202603355 
  + Hoàng Ngọc Minh Trí - 2A202603379 
  + Chử Thị Ánh - 2A202603360
  + Hoàng Văn Bảo - 2A202603549
  + Trần Thành Nam - 2A202603564
- Provider/model: OpenRouter / openai/gpt-4o-mini

---

# PHẦN A — Giới thiệu agent

**Research Agent — tìm tin, đọc bài và tổng hợp bản tin**

**Bản demo hiện tại: 11 tool · 1 tool nhóm tự viết · 210 test PASS.**

## A1. Agent này làm được gì

Research Agent giúp bạn tìm tin trên web, theo dõi bài đăng trên X/Twitter, đọc bài từ một đường link và tổng hợp kết quả thành bản tin có nguồn. Agent cũng hỗ trợ tìm bài nghiên cứu trên arXiv, tra cứu chính sách nội bộ, lọc URL trùng và gửi bản tin qua Telegram khi đã được xác nhận.

**Mở demo:** [Research Agent](https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app)

Để dùng thử, nhập yêu cầu vào ô chat. Nếu agent hỏi thêm tài khoản hoặc URL, bạn trả lời ở lượt tiếp theo; khi muốn đổi chủ đề, chọn **Cuộc trò chuyện mới**.

Bản demo chạy trên Streamlit Community Cloud nên bạn vẫn có thể truy cập khi máy cá nhân của nhóm đã tắt. Sau một thời gian không sử dụng, app có thể cần chờ khởi động lại. Các công cụ gọi dịch vụ bên ngoài vẫn phụ thuộc vào API key và hạn mức.

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

Nhóm bổ sung **`deduplicate`** để xử lý trường hợp nhiều danh sách tìm kiếm cùng chứa một URL. Tool giữ bản ghi đầu tiên, bỏ các URL lặp lại và giữ thứ tự ban đầu. Phần này chạy cục bộ, không cần API key.

**Kết quả kiểm thử:** Bộ test offline đạt **210 PASS, 0 FAIL, 0 ERROR, 0 SKIP**. Các test kiểm tra khai báo tool có khớp code hay không, cách xử lý đầu vào và các tình huống lỗi. Lời gọi HTTP được mô phỏng bằng mock, vì vậy kết quả này chưa thay thế cho thử nghiệm với API thật. Riêng Telegram cần cấu hình bot/kênh và có xác nhận của người dùng trước khi gửi.

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

## B1. Quá trình cải thiện qua từng phiên bản

Nhóm dùng **OpenRouter / openai/gpt-4o-mini** cho các lần đánh giá dưới đây. Số liệu được đối chiếu với run JSON và `version_log.csv` để có thể xem lại từng thay đổi và kết quả.

> **Lưu ý về tiến trình phiên bản và khoảng trống v4:**
> Tiến trình thực thi không diễn ra tuyến tính liên tục qua từng số phiên bản mà chuyển trực tiếp từ **v3** sang **v5-tools-complete**. Phiên bản **v4** là vòng lặp nội bộ (thử nghiệm gộp code tool và chỉnh sửa cục bộ) không chạy riêng một lượt eval độc lập, mà được hoàn thiện và tích hợp toàn diện trực tiếp vào phiên bản **v5-tools-complete**. Do đó, dữ liệu đánh giá và bằng chứng định lượng chỉ tồn tại cho các lượt chạy thực tế có file run JSON lưu trong thư mục `starter_v0/runs/`: `v0`, `v1`, `v2`, `v2-fix`, `v3`, `v5-tools-complete`, `v5-evalfix`, và `v6-date-context`.

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
| v6-date-context | base | tools.yaml; lookup; runtime chat/UI | Đo lại chọn tool và args sau sửa; eval không chạy context ngày giờ của chat/UI | 95% (v5-tools-complete) | 18/20 case đo được (90%) | [v6-date-context_B_base_openrouter_20261110T170026806316.json](../runs/v6-date-context_B_base_openrouter_20261110T170026806316.json) |
| v6-date-context | group | tools.yaml; lookup; runtime chat/UI | Đo lại chọn tool và args sau sửa; eval không chạy context ngày giờ của chat/UI | 100% (v5-evalfix) | 10/10 case đo được (100%) | [v6-date-context_B_group_openrouter_20261110T170120261117.json](../runs/v6-date-context_B_group_openrouter_20261110T170120261117.json) |

| Bản đo | Case PASS | Routing | Arguments | Multi turn | Case không đo được |
|---|---|---|---|---|---|
| Base — v5-tools-complete | 19/20 | 100% | 95% | 100% | 0 |
| Group — v5-evalfix | 10/10 | 100% | 100% | 100% | 0 |
| Base — v6-date-context | 18/20 | 100% | 90% | 100% | 0 |
| Group — v6-date-context | 10/10 | 100% | 100% | 100% | 0 |

Cần đọc điểm cùng với số case thực sự đo được. Ở lần group đầu, màn hình hiện accuracy 100% nhưng chỉ có 9 case được chấm; G01 gặp lỗi trong bộ so sánh và bị ghi nhãn `provider_error`. Sau khi sửa bộ chấm, lần chạy lại mới đạt đủ 10/10 PASS. Nhóm giữ nguyên nội dung case trong quá trình này. Base và group là hai bộ dữ liệu riêng, nên không so trực tiếp hai mức điểm như cùng một bài kiểm tra.

Từ v0 đến v3, nhóm giữ nguyên khai báo tool và tập trung chỉnh prompt. Đến v5, mô tả tool, kiểm tra đầu vào và tool mới được cập nhật cùng lúc. Điểm 95% cho thấy kết quả của cả đợt thay đổi, nhưng chưa cho biết riêng phần nào đóng góp bao nhiêu. Khi chạy lại, cần đối chiếu `artifact_version` của prompt/tools.yaml cùng code tool và bộ chấm trong repo.

## B2. Những lỗi đã gặp và cách xử lý

Bảng dưới đây ghi lại các case FAIL và điều thực sự xảy ra trong log. Một số case là lỗi chọn tool hoặc tham số của model; một số khác cần xem lại cách chấm. Nhóm giữ cả kết quả lỗi để giải thích quá trình sửa.

| Version/suite | Case | Nhãn lỗi | Lỗi quan sát | Tool call thực tế | Phân tích / xử lý |
|---|---|---|---|---|---|
| v0/base | R08_out_of_scope | out_of_scope | unexpected_tool_call | `send({"text":"Nguyên hàm của x^2 là \\( \\frac{x^3}{3} + C \\), trong đó \\( C \\) là hằng số tùy ý."})` | Agent gọi tool dù yêu cầu nằm ngoài phạm vi. Các lần chạy sau đã PASS, nhưng nhóm chưa thử riêng từng quy tắc để xác định yếu tố nào giúp cải thiện. |
| v0/base | R10_missing_handle | missing_info | missing_tool_call | `timeline({"screenname":"sama"})` | Agent tự điền thông tin người dùng chưa cung cấp. v1 thêm yêu cầu hỏi lại, nhưng v2 sửa nhầm đoạn này khiến lỗi quay lại. Base ở bản sau đã PASS; phiên chat thật vẫn cho thấy hành vi tương tự cần được kiểm tra thêm. |
| v0/base | R11_missing_url | missing_info | missing_tool_call | `fetch({"url":"https://example.com/article"})` | Agent tự điền thông tin người dùng chưa cung cấp. v1 thêm yêu cầu hỏi lại, nhưng v2 sửa nhầm đoạn này khiến lỗi quay lại. Base ở bản sau đã PASS; phiên chat thật vẫn cho thấy hành vi tương tự cần được kiểm tra thêm. |
| v0/base | R12_confirm_before_send | wrong_boundary | missing_tool_call | `send({"text":"Bản tin này đã được đăng lên Telegram."})` | Agent chọn send khi chưa hỏi xác nhận; hành vi mong đợi là clarify(yes_no). Log tool call chưa đủ để kết luận tin nhắn đã được gửi thật. |
| v0/base | R13_parallel_web_and_tweets | wrong_tool | wrong_arg_value | `lookup({"query":"AI news","timeframe":"day","max_results":5})`; `social_search({"query":"AI","search_type":"Latest","limit":5})` | Tên lỗi là wrong_tool, nhưng observed_mismatch cho thấy lệch ở query/topic. Nhóm làm rõ cách chọn nguồn và quy ước news; bản sau đã PASS. |
| v0/base | R14_out_of_scope_coding | out_of_scope | unexpected_tool_call | `send({"text":"Dưới đây là một hàm Python tính số Fibonacci bằng đệ quy:\n\n```python\ndef fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n     ...)` | Agent gọi tool dù yêu cầu nằm ngoài phạm vi. Các lần chạy sau đã PASS, nhưng nhóm chưa thử riêng từng quy tắc để xác định yếu tố nào giúp cải thiện. |
| v1/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung bản tin mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi người dùng cung cấp nội dung bằng clarify(text), còn đáp án yêu cầu yes_no. Vì yêu cầu chưa có nội dung bản tin, case này cần được đọc lại thủ công. Log không cho thấy agent gửi ngay. |
| v1/base | M02_carryover_timeframe | wrong_arg_value | missing_tool_call | `social_search({"query":"robotics","search_type":"Latest","limit":5})` | Agent chuyển sang social_search dù người dùng đang hỏi tin web. Nguồn và khoảng thời gian cần được giữ từ lượt trước; base ở bản sau đã PASS. |
| v2/base | R10_missing_handle | missing_info | missing_tool_call | `timeline({"screenname":"twitter","limit":5})` | Agent tự điền thông tin người dùng chưa cung cấp. v1 thêm yêu cầu hỏi lại, nhưng v2 sửa nhầm đoạn này khiến lỗi quay lại. Base ở bản sau đã PASS; phiên chat thật vẫn cho thấy hành vi tương tự cần được kiểm tra thêm. |
| v2/base | R11_missing_url | missing_info | missing_tool_call | `fetch({"url":"https://"})` | Agent tự điền thông tin người dùng chưa cung cấp. v1 thêm yêu cầu hỏi lại, nhưng v2 sửa nhầm đoạn này khiến lỗi quay lại. Base ở bản sau đã PASS; phiên chat thật vẫn cho thấy hành vi tương tự cần được kiểm tra thêm. |
| v2-fix/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi người dùng cung cấp nội dung bằng clarify(text), còn đáp án yêu cầu yes_no. Vì yêu cầu chưa có nội dung bản tin, case này cần được đọc lại thủ công. Log không cho thấy agent gửi ngay. |
| v2-fix/base | R13_parallel_web_and_tweets | wrong_tool | wrong_arg_value | `lookup({"query":"AI","timeframe":"day","max_results":5})`; `social_search({"query":"AI","limit":5})` | Tên lỗi là wrong_tool, nhưng observed_mismatch cho thấy lệch ở query/topic. Nhóm làm rõ cách chọn nguồn và quy ước news; bản sau đã PASS. |
| v2-fix/base | M02_carryover_timeframe | wrong_arg_value | missing_tool_call | `social_search({"query":"robotics","search_type":"Latest","limit":5})` | Agent chuyển sang social_search dù người dùng đang hỏi tin web. Nguồn và khoảng thời gian cần được giữ từ lượt trước; base ở bản sau đã PASS. |
| v2-fix/base | M06_switch_tool | wrong_tool | missing_tool_call | `social_search({"query":"OpenAI","search_type":"Latest","limit":5})` | Khi người dùng chuyển từ X sang web, agent vẫn dùng nguồn X hoặc gọi thêm social_search. Base ở bản sau và G09 của group đã PASS. |
| v3/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi người dùng cung cấp nội dung bằng clarify(text), còn đáp án yêu cầu yes_no. Vì yêu cầu chưa có nội dung bản tin, case này cần được đọc lại thủ công. Log không cho thấy agent gửi ngay. |
| v3/base | M06_switch_tool | wrong_tool | extra_tool_call | `lookup({"query":"OpenAI","topic":"news","timeframe":"day","max_results":5})`; `social_search({"query":"OpenAI","search_type":"Latest","limit":5})` | Khi người dùng chuyển từ X sang web, agent vẫn dùng nguồn X hoặc gọi thêm social_search. Base ở bản sau và G09 của group đã PASS. |
| v5-tools-complete/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"question":"Bạn có thể cung cấp nội dung cụ thể mà bạn muốn đăng lên Telegram không?","response_type":"text"})` | Agent hỏi người dùng cung cấp nội dung bằng clarify(text), còn đáp án yêu cầu yes_no. Vì yêu cầu chưa có nội dung bản tin, case này cần được đọc lại thủ công. Log không cho thấy agent gửi ngay. |
| v5-tools-complete/group | G01_deduplicate_items | provider_error | provider_error | Không có tool call được lưu | normalize_value sắp xếp list[dict] bằng sorted nên phát sinh TypeError; lỗi bị ghi nhầm thành provider_error. Nhóm sửa bộ so sánh, thêm 9 test và chạy lại group đạt 10/10. |
| v6-date-context/base | R03_web_news_routing | wrong_tool | wrong_arg_value | `lookup({"query":"tin tức AI","topic":"news","timeframe":"day"})` | Agent chọn đúng tool, topic và timeframe. Case FAIL vì query khác chuỗi `AI` trong đáp án; đây là lệch tham số, không phải chọn nhầm tool. |
| v6-date-context/base | R12_confirm_before_send | wrong_boundary | wrong_arg_value | `clarify({"response_type":"text"})` — hỏi nội dung cụ thể để đăng | Đáp án yêu cầu yes_no, trong khi agent hỏi thêm nội dung. Do yêu cầu chưa kèm bản tin, cần xem xét thủ công; case này không có lệnh send. |
| Live CLI | Lượt 2 | missing_info — đánh giá thủ công | Tự suy diễn account | `timeline({"screenname":"robotics","limit":2})` | Agent lấy chủ đề robotics ở lượt trước làm tên tài khoản. Đúng ra cần hỏi người dùng muốn xem account nào. Phiên này chưa xử lý đúng tình huống đó. |

## B3. Bộ câu hỏi đánh giá của nhóm

Nhóm xây dựng **10 case: 5 single turn và 5 multi turn** để kiểm tra chọn tool, truyền tham số và xử lý hội thoại. Bảng dưới đây dùng kết quả từ [v5-evalfix_B_group_openrouter_20261110T144452606199.json](../runs/v5-evalfix_B_group_openrouter_20261110T144452606199.json).

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

Ở G01, model cần chọn `deduplicate` và truyền đầy đủ danh sách ban đầu; việc lọc trùng có đúng hay không được kiểm tra bằng unit test riêng. G10 cung cấp sẵn nội dung và đích gửi nên yêu cầu xin xác nhận rõ hơn R12 của base. Bộ group hiện chưa bao phủ tình huống đổi từ chủ đề web sang yêu cầu bài đăng X mà thiếu account; nhóm phát hiện khoảng trống này khi chat thật.

## B4. Kết quả thử hội thoại thực tế

Transcript CLI: [v5-evalfix_openrouter_20261110T144638732811.transcript.json](../transcripts/v5-evalfix_openrouter_20261110T144638732811.transcript.json). Artifact: `v5-evalfix+pcf82e7a93a6b+t1dfc05a44ef2`. Phiên có **3 lượt live** và kết thúc bằng `/exit`.

| Lượt | Yêu cầu | Tool call thực tế | Trạng thái chạy | Đánh giá thủ công |
|---|---|---|---|---|
| 1 | Tìm 3 tin tức về robotics trên web trong tuần này, kèm nguồn. | `lookup({"query":"robotics","topic":"news","timeframe":"week","max_results":3})` | answered | Agent chọn đúng lookup(news, week, 3), nhận 3 kết quả và trả lời kèm nguồn. Nhóm chưa đối chiếu thủ công từng bài gốc. |
| 2 | Lấy 2 bài đăng mới nhất trên X giúp tôi. | `timeline({"screenname":"robotics","limit":2})` | answered | Chưa đúng: agent tự chọn account robotics từ chủ đề trước thay vì hỏi lại. Tool lấy được dữ liệu, nhưng dữ liệu đó chưa đáp ứng đúng ý người dùng. |
| 3 | Tài khoản nasa. | `timeline({"screenname":"nasa","limit":2})` | answered | Agent đổi account sang nasa, giữ limit=2 và nhận 2 kết quả. Lượt này cho thấy agent tiếp nhận thông tin được sửa; lượt 2 vẫn chưa hỏi lại đúng. |

Phiên chat cho thấy cần đọc cả nội dung và tool call, vì `status=answered` chỉ báo đã có câu trả lời. Agent cũng trả lời bằng tiếng Anh dù người dùng hỏi tiếng Việt; nhóm cần cải thiện điểm này để bản demo dễ sử dụng hơn.

## B4.1. Thử lại trên Cloud sau khi sửa ngày — v6-date-context

Transcript tải từ UI: [ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json](../transcripts/ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json), có **2 lượt**, đều `answered`. Artifact Cloud: `v6-date-context+pc5fd2628fcf2+t190818f266ea`. Mỗi lượt có `runtime_context.current_date=2026-11-10`, `utc_offset=+07:00`.

| Lượt | Quan sát từ transcript | Đánh giá thủ công |
|---|---|---|
| 1 — Giá vàng hôm nay | `lookup(query="giá vàng", topic="general", max_age_hours=0)`, không truyền timeframe; retrieved_at=2026-11-10T16:54:45+07:00. Kết quả PNJ/BTMC không có published_date trong log. | Ngày giờ đã đúng và tool được yêu cầu lấy live. Tuy vậy, query chưa ghi ngày cụ thể, nguồn chưa đủ thông tin về thời điểm và đơn vị. Câu trả lời vẫn gọi là giá hôm nay và gán VNĐ, nên chưa đạt yêu cầu kiểm chứng giá. |
| 2 — Ngày hiện tại và giá xăng | Trả lời đúng 10/11/2026. Gọi lookup cho giá xăng và một lookup khác cho ngày hiện tại; không truyền max_age_hours. Nguồn VnExpress hiển thị 07/11/2026, bảng ghi giá từ 15:00 05/11/2026. | Agent trả lời đúng ngày. Với giá xăng, chưa kiểm tra bảng giá 05/11 có còn hiệu lực ngày 10/11 hay không. Ngày áp dụng cũ chưa có nghĩa giá sai, nhưng cần xác minh trước khi gọi là giá hiện tại. Lượt tìm ngày hiện tại cũng không cần thiết vì đã có runtime_context. |

**Kết quả đối chiếu artifact:** hai run eval v6 dùng `pcf82e7a93a6b+t0bedf4dee6f6`, transcript Cloud dùng `pc5fd2628fcf2+t190818f266ea`. Chuẩn hóa CRLF thành LF trên local cho đúng cả hai hash Cloud, nên prompt/tools khớp nội dung; `versioning.py` đang hash bytes nguyên bản. Hai remote ntc cùng commit `9b3cc29` tại lúc kiểm tra. Giữ nguyên hash lịch sử. Điểm 90%/100% vẫn là điểm của eval, không phải điểm phiên UI/giá live vì đường chạy khác. Chi tiết: [artifact_comparison.md](artifact_comparison.md).

Qua hai lượt này, có thể xác nhận app đã truyền đúng ngày UTC+7 và model trả lời đúng ngày ở lượt 2. Prompt/tools cũng đã được đối chiếu khớp nội dung. Phần nguồn giá vẫn cần xử lý thêm, nên nhóm giữ nguyên transcript và chưa đánh giá cả phiên là thành công chỉ dựa vào `status=answered`.

## B4.2. Bằng chứng thực tế kịch bản xác nhận gửi — live_send_confirmation

Transcript live: [live_send_confirmation.transcript.json](../transcripts/live_send_confirmation.transcript.json). Artifact: `v7-send-confirmation`.

| Lượt | Yêu cầu người dùng | Hành vi / Tool Call | Trạng thái | Đánh giá guardrail |
|---|---|---|---|---|
| 1 | Đăng bản tin sau lên kênh Telegram @research_channel: Báo cáo ngày 11/11/2026: Đã hoàn thành baseline và các bài test. Hãy hỏi tôi xác nhận trước khi gửi. | `clarify({"response_type":"yes_no","draft":"...","destination":"@research_channel"})` | `waiting_for_user` | **Đạt guardrail**: Agent không tự ý gọi `send` ngay mà kích hoạt clarify(yes_no), hiển thị bản nháp và kênh đích cụ thể để người dùng duyệt. |
| 2 | `yes` | `send({"confirmed":true,"destination":"@research_channel","text":"..."})` | `send_error` | **Đạt guardrail**: Sau khi người dùng xác nhận rõ ràng bằng `yes`, agent mới thực thi gọi tool `send`. Hệ thống bảo vệ an toàn (chặn hoặc thông báo cấu hình token môi trường) mà không làm crash phiên. |

## B5. Hoàn thiện tool, giao diện và kiểm thử

| Hạng mục | Bằng chứng | Kết quả và giới hạn |
|---|---|---|
| Tool mới deduplicate | tools/deduplicate/; G01; tests/test_tools_todo.py | Đã có implementation, TOOL.md, registry và schema; G01 PASS. Lọc theo URL, không phát hiện trùng nội dung khác URL. |
| Telegram send | tests/test_tool_validation.py; tests/test_tools_todo.py; G10; transcripts/live_send_confirmation.transcript.json | Guardrail và gửi HTTP bằng mock PASS; G10 hỏi xác nhận PASS. Đã bổ sung transcript live chứng minh luồng chặn duyệt draft/destination trước khi gọi send. |
| arXiv / policy | tests/test_tool_validation.py; tests/test_tools_todo.py | Test metadata, retry 429, PDF cục bộ và trust boundary PASS. Không dùng test mock để khẳng định mọi API live hoạt động. |
| UI | app.py; transcripts/ui_*.transcript.json; link ở Phần A | Đã có UI, transcript theo phiên và triển khai Streamlit Cloud. Transcript cũ giữ nguyên; B4.1 bổ sung transcript Cloud v6 gồm 2 lượt, đúng ngày nhưng còn giới hạn về nguồn giá; hash khác eval chỉ do LF/CRLF. |
| Test offline | tests/; artifacts/tools_unit_tests.txt | 210 PASS, 0 FAIL, 0 ERROR, 0 SKIP: 175 test tool trước đó, 9 test bộ chấm và 26 test ngày giờ/độ mới nguồn. |
| Sửa bộ chấm eval | run_eval.py; tests/test_eval_structured_args.py; hai group run JSON | Giữ so sánh scalar list không phụ thuộc thứ tự; list object/nested list giữ thứ tự. Không đổi dữ liệu eval để né lỗi. |

Nhóm đã điền đủ 17 test TODO, mỗi test có assertion để kiểm tra hành vi. Các lời gọi HTTP được mock nên chạy offline, không tiêu credit hay gửi Telegram thật. Năm test PDF dùng thư mục tạm riêng để tránh lỗi quyền truy cập `pytest-of-Admin` trên Windows.

Trong lúc viết test, nhóm phát hiện và giữ lại test cho các lỗi sau:

- `send` từng chấp nhận chuỗi `"false"`, `"true"` và số `1` như xác nhận. Bản sửa chỉ chấp nhận boolean `True`, kiểm tra `ok=true` của Telegram và che token trong lỗi.
- `timeline` từng truyền nguyên handle có khoảng trắng/@ và có thể thiếu URL khi API không trả handle. Bản sửa chuẩn hóa handle và dựng URL từ account đã biết.
- `paper_text` từng áp tối thiểu 1000 ký tự, làm sai yêu cầu `max_chars=4`. Bản sửa tôn trọng giới hạn dương.

Các test được chọn cho ba lỗi trên cho kết quả **5 FAIL, 3 PASS trên code cũ** và đều PASS sau khi sửa. Log trước sửa nằm ở `artifacts/tools_regression_before.txt`. Với 9 test bổ sung cho bộ chấm, kết quả trước sửa là **8 FAIL, 1 PASS**; sau sửa, cả 9 đều PASS. Test CLI offline cũng xác nhận `deduplicate` thực thi và tạo run có measured_cases=1 thay vì provider_error.

Những lỗi này cho thấy cần cả model eval lẫn unit test. Eval có thể ghi nhận đúng tên `send` và tham số, còn unit test kiểm tra chuỗi `"false"` có bị chặn trước khi gửi hay không. Tương tự, code deduplicate đã qua unit test nhưng G01 vẫn lỗi vì bộ chấm cũ không xử lý được danh sách object.

### B5.1. Bổ sung kiểm tra ngày hiện tại — v6-date-context

Khi thử giá vàng trên Cloud ngày 10/11/2026, agent lại ghi “hôm nay” là 07/11/2026. Nhóm kiểm tra code và thấy vòng chat chưa truyền ngày hiện tại cho model, lookup mặc định lọc theo tuần và bỏ trường ngày của nguồn. Do chưa có transcript riêng của lượt lỗi ban đầu, nhóm chưa xác định được chính xác model đã gửi tham số nào.

Bản sửa bổ sung giờ Việt Nam UTC+7 ở mỗi lượt, lưu `runtime_context` trong transcript và hiển thị ngày trên UI. Lookup giữ `published_date` khi API có trả, bỏ mặc định lọc theo tuần và thêm `max_age_hours=0` để yêu cầu lấy trang live khi cần dữ liệu cập nhật liên tục. Model cũng được hướng dẫn phân biệt ngày của nguồn với giờ truy xuất, đồng thời nói rõ nếu chưa xác minh được thời điểm của số liệu.

Nhóm thêm **26 test** cho chuyển ngày UTC/Vietnam, phiên qua nửa đêm, thông tin lưu ở các nhánh kết thúc và dữ liệu thời gian gửi/nhận từ tool; tổng bộ test đạt **210 PASS**. Transcript ở B4.1 cho thấy ngày đã đúng, nhưng giá hiện tại vẫn chưa được xác minh đầy đủ.

Hai run v6 đạt base **18/20 (90%)** và group **10/10 (100%)**, không có provider_error. So với lần base v5 đã lưu, điểm giảm 5 điểm phần trăm. Hai lần chạy chưa đủ để kết luận riêng thay đổi ngày giờ gây giảm điểm; R03 lệch query và R12 lệch response_type như đã phân tích ở B2.

Một giới hạn cần lưu ý là eval gọi `ResearchAgent.run` trực tiếp, còn CLI/UI dùng `run_model_tool_loop` có context ngày giờ. Vì vậy, điểm eval phản ánh việc chọn tool và tham số ở bản v6, chưa kiểm tra toàn bộ vòng chat hay độ đúng của giá vàng hôm nay. Chi tiết sửa lỗi được lưu trong [date_context_fix.md](date_context_fix.md).

## B6. Điều nhóm rút ra sau bài lab

Qua các vòng sửa prompt, nhóm thấy việc hỏi lại, xin xác nhận và giữ ngữ cảnh cần được diễn đạt rõ. Lần v2 thay nhầm đoạn hỏi thông tin khiến lỗi quay lại, dù mục đích ban đầu là bổ sung xác nhận. Từ đó, nhóm cần lưu bản prompt trước mỗi lần sửa và đọc diff trước khi chạy để biết mình đang kiểm chứng giả thuyết nào.

Mô tả trong tools.yaml giúp model hiểu khi nào dùng từng tool và truyền tham số theo quy ước nào. Tuy nhiên, code vẫn phải kiểm tra đầu vào. Trường hợp send nhận chuỗi false như một xác nhận hợp lệ cho thấy mô tả đúng chưa đủ để đảm bảo hành động đúng.

Nhóm cũng học được rằng phải đọc log trước khi kết luận từ điểm số. R12 hỏi thêm nội dung nhưng đáp án chỉ chấp nhận yes_no; lỗi TypeError của bộ chấm lại bị ghi thành provider_error. Trong phiên chat thật, agent có thể trả lời và lấy được dữ liệu nhưng vẫn chọn nhầm account. Những tình huống này cần được ghi rõ thay vì chỉ nhìn PASS/FAIL hoặc trạng thái answered.

Base và group đều là các tập nhỏ; group do nhóm tự thiết kế, trong đó có yêu cầu gọi tên tool khá rõ. Vì thế, điểm group 100% chưa cho biết agent đáng tin cậy đến đâu với yêu cầu mới. Phiên live đã bộc lộ lỗi lấy chủ đề làm handle mà bộ group chưa có case kiểm tra.

Việc cần làm tiếp là bổ sung regression cho chuỗi “tin robotics trên web → lấy bài trên X nhưng chưa nêu account”, kiểm tra lại xử lý nguồn giá và cho agent trả lời cùng ngôn ngữ người dùng. Các việc này chưa có kết quả mới trong báo cáo. Khi bàn giao, nhóm giữ cả log lỗi lẫn log thành công, đối chiếu hash cùng code bộ chấm và kiểm tra thông tin nhạy cảm trước khi đưa lên repo.

## B7. Small Local Model Challenge (bonus)

Nhóm chưa chạy Ollama trong phần bằng chứng hiện có nên chưa có kết quả so sánh cloud/local. Phần bonus này chưa được thực hiện và chưa được tính vào kết quả báo cáo.

## B8. Phân công công việc tiếp theo

Bảng dưới đây là phương án phân công dự kiến dựa trên những việc còn lại trong báo cáo. Nhóm sẽ bàn lại trước khi chốt người phụ trách; bảng này không dùng để xác định ai đã làm các phần trước đó.

| Thành viên | Phụ trách chính | Đầu ra |
|---|---|---|
| Cường | Eval, version evidence, tích hợp và báo cáo B1/B2/B6 | Metric khớp run JSON; tổng hợp REPORT/version log và review. |
| Trí | UI, deploy, giới thiệu A1–A3 và demo B4 | Link Cloud, kịch bản demo, transcript của bản triển khai. |
| Ánh | Prompt/hội thoại, clarify và xác nhận send | Sửa suy diễn topic thành handle, tiếng Việt, hỏi/xác nhận đúng ngữ cảnh; bằng chứng trước/sau. |
| Bảo | Lookup/fetch, ngày hiệu lực và đơn vị của giá | Kiểm tra nguồn cũ/thiếu đơn vị; không khẳng định giá hôm nay khi chưa xác minh. |
| Nam | QA tools, regression và group B3/B5 | Test có assertion, case bổ sung, log pytest và eval trên bản tích hợp. |