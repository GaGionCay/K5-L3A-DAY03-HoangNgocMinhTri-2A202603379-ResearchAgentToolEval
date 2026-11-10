# Team — Day 03: Research Agent Tool Eval

**Bản dự thảo tổng kết theo phân vai.** Các mục đóng góp và nhận xét bên dưới được soạn theo tình huống nhóm đã hoàn thành để từng thành viên rà soát, xác nhận trước khi nộp. Đây chưa phải xác nhận đóng góp thực tế của mọi người. Nhóm cần đối chiếu với file, run/test log và commit; phần bằng chứng đã xác minh được ghi riêng ở cuối tài liệu.

## Thông tin nhóm

- Tên nhóm: HoangNgocMinhTri - 2A202603379.
- Bài tập: Day 03 — Prompt Engineering & Tool Calling, Research Agent Tool Eval.
- Mục tiêu: Xây dựng research agent có thể chọn tool, truyền tham số, tìm và đọc thông tin; cải thiện hành vi qua nhiều phiên bản dựa trên log đánh giá.
- Repository chung: [GaGionCay/ResearchAgentToolEval](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval).
- Báo cáo nhóm: [starter_v0/artifacts/REPORT.md](starter_v0/artifacts/REPORT.md).
- Phạm vi tổng kết: Đánh giá phiên bản, prompt/tool declaration, phát triển tool, eval/unit test, demo và báo cáo.

## Thành viên

| STT | Họ và tên | MSSV | Vai trò trong nhóm | Tài khoản GitHub | Branch cá nhân |
|---:|---|---|---|---|---|
| 1 | Chử Thị Ánh | 2A202603360 | Phần 1 — Đánh giá và quản lý phiên bản | chuthia8@gmail.com | chuthianh |
| 2 | Hoàng Ngọc Minh Trí | 2A202603379 | Phần 2 — Prompt và khai báo tool | minhtrihoangngoc@gmail.com | hmt |
| 3 | Hoàng Văn Bảo | 2A202603549 | Phần 3 — Phát triển tool | mailto:26ai.baohv@vinuni.edu.vn | bao |
| 4 | Trần Thành Nam | 2A202603564 | Phần 4 — Eval và unit test | thanhnam120304@gmail.com | nam |
| 5 | Nguyễn Thế Cường | 2A202603355 | Phần 5 — Demo và báo cáo | ntcuong1113@gmail.com | cuong |


## Tổng hợp phân công và đầu ra

| Phần việc | Người chính | Công việc tổng kết | Đầu ra để đối chiếu |
|---|---|---|---|
| 1 — Đánh giá và quản lý phiên bản | Chử Thị Ánh | Thiết lập môi trường, chạy preflight và baseline; phân loại lỗi, phối hợp đánh giá v1–v3, ghi giả thuyết và kết quả. | Run JSON v0–v3, version_log.csv, bảng phân tích lỗi. |
| 2 — Prompt và khai báo tool | Hoàng Ngọc Minh Trí | Điều chỉnh routing, hỏi lại, giữ ngữ cảnh, quy ước tham số và xác nhận trước khi gửi. | system_prompt.md, tools.yaml và giải thích thay đổi trước/sau. |
| 3 — Phát triển tool | Hoàng Văn Bảo | Triển khai tool mới, viết hướng dẫn, đăng ký schema/registry và xử lý lỗi code tool. | tool.py, TOOL.md, tools/__init__.py và khai báo tương ứng trong tools.yaml. |
| 4 — Eval và unit test | Trần Thành Nam | Xây dựng case nhóm, test tool mới, hoàn thiện test TODO và kiểm tra hồi quy. | eval_group.json, tests/, run JSON và kết quả pytest. |
| 5 — Demo và báo cáo | Nguyễn Thế Cường | Chuẩn bị UI/link, thử hội thoại, lưu transcript và tổng hợp nội dung báo cáo nhóm. | app.py, dependency UI, link demo, transcript và REPORT.md. |

Bộ eval nhóm cần 10 case, gồm 5 single turn và 5 multi turn, theo README. Mỗi tool mới cần ít nhất 3 unit test. Kết quả chạy và số case thực sự đo được phải lấy từ log, không suy ra chỉ từ số lượng case đã viết.

## Cá nhân — nội dung tổng kết và bằng chứng thực tế

> **Quy ước rà soát:** Mỗi phần dưới đây phân tách rành mạch giữa **Công việc đã hoàn thành & có bằng chứng kiểm thử** (kèm file/run log thực tế đối chiếu với REPORT.md) và **Phần việc mở / định hướng tiếp theo** (chưa hoàn thành hoặc còn giới hạn).

### ChuThiAnh-2A202603360

**Phần việc phụ trách:** Phần 1 — Đánh giá, quản lý phiên bản & Gemini Provider.

**Đóng góp cụ thể:**

- **Đã hoàn thành & có bằng chứng:**
  - Thiết lập môi trường đánh giá baseline ban đầu trên Gemini và tham gia chạy/ghi nhận các vòng đánh giá phiên bản (`v0` đến `v3`, `v5`, `v6`).
  - Viết và tích hợp tool `keyword_extract` (`starter_v0/tools/keyword_extract/tool.py`, `TOOL.md`), đăng ký trong hệ thống.
  - Đóng góp cơ chế retry cho Gemini provider khi gặp lỗi rate limit (`starter_v0/providers/gemini_provider.py`).
  - Ghi nhận và theo dõi các chỉ số qua [version_log.csv](starter_v0/artifacts/version_log.csv) cùng các run JSON tương ứng trong `starter_v0/runs/`.
- **Giới hạn & Việc mở / Tiếp theo (B8):**
  - Run baseline Gemini ban đầu có 1 provider error (`v0_B_base_gemini_20261110T123153716162.json`).
  - Nhận nhiệm vụ tiếp tục hoàn thiện prompt xử lý suy diễn topic thành handle khi chuyển từ web sang X, hỗ trợ tiếng Việt nhất quán và xác nhận send đúng ngữ cảnh.

**Bằng chứng đối chiếu:**
- `starter_v0/runs/`: các run baseline và version logs tương ứng.
- [starter_v0/artifacts/version_log.csv](starter_v0/artifacts/version_log.csv), REPORT.md (Mục B1, B2).
- Commit trên branch `chuthianh`: `c4a2e08`, `8dadbb6`.

---

### HoangNgocMinhTri-2A202603379

**Phần việc phụ trách:** Phần 2 — Prompt, khai báo tool, UI demo & kịch bản hội thoại.

**Đóng góp cụ thể:**

- **Đã hoàn thành & có bằng chứng:**
  - Tối ưu `system_prompt.md` và `tools.yaml` qua các phiên bản v1–v3 và v6: làm rõ quy tắc định tuyến cho `lookup`, `timeline`, `social_search`, `fetch`, `clarify` và nhóm Bonus Tools (`policy`, `papers`, `paper_text`, `format`, `deduplicate`).
  - Chuẩn hóa ranh giới an toàn cho thao tác gửi: chặn mô hình tự gửi, bắt buộc gọi `clarify` với `response_type="yes_no"` kèm `draft` và `destination`.
  - Triển khai và vận hành giao diện Streamlit Cloud demo công khai: [Research Agent App](https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app).
  - Thực hiện và lưu trữ transcript live cho kịch bản bảo vệ xác nhận gửi: [live_send_confirmation.transcript.json](starter_v0/transcripts/live_send_confirmation.transcript.json) (được ghi nhận tại REPORT B4.2).
- **Giới hạn & Việc mở / Tiếp theo (B8):**
  - Prompt chưa giải quyết triệt để lỗi khi người dùng chuyển từ web sang bài đăng X mà không cung cấp account (agent vẫn có xu hướng tự lấy query web làm screenname ở lượt chat thực tế).
  - Tiếp tục hoàn thiện kịch bản demo và tài liệu giới thiệu Phần A1–A3.

**Bằng chứng đối chiếu:**
- [starter_v0/artifacts/system_prompt.md](starter_v0/artifacts/system_prompt.md), [starter_v0/artifacts/tools.yaml](starter_v0/artifacts/tools.yaml).
- Link Streamlit Cloud trong REPORT Phần A1.
- [starter_v0/transcripts/live_send_confirmation.transcript.json](starter_v0/transcripts/live_send_confirmation.transcript.json).
- Commit trên branch `hmt`: `62f7eb3`, `7b4ff28`.

---

### HoangVanBao-2A202603549

**Phần việc phụ trách:** Phần 3 — Phát triển tool, kiểm tra đầu vào và ranh giới dữ liệu.

**Đóng góp cụ thể:**

- **Đã hoàn thành & có bằng chứng:**
  - Tham gia rà soát và củng cố logic kiểm tra tham số, validation biên cho các tool lõi và tool nghiên cứu (`tools/_validation.py`, `tools/fetch/tool.py`, `tools/papers/tool.py`, `tools/lookup/tool.py`).
  - Đảm bảo các tool tương tác bên ngoài sử dụng khóa API an toàn qua biến môi trường (`TAVILY_API_KEY`, `FIRECRAWL_API_KEY`, `ARXIV_USER_AGENT`), không để lộ token.
  - Phối hợp xác thực đồng bộ registry trong `tools/__init__.py` và `tools.yaml`.
- **Giới hạn & Việc mở / Tiếp theo (B8):**
  - Chưa xử lý triệt để việc xác minh thời điểm và đơn vị giá khi tra cứu giá vàng/giá xăng live (kết quả web search trả về nguồn hiển thị ngày cũ hoặc thiếu đơn vị cụ thể, chưa kiểm chứng độ tươi tuyệt đối).
  - Nhận nhiệm vụ tiếp tục hoàn thiện kiểm tra nguồn cũ/thiếu đơn vị trong `lookup` và `fetch` ở các vòng tối ưu tiếp theo.

**Bằng chứng đối chiếu:**
- `starter_v0/tools/`: code implementation và file TOOL.md tương ứng.
- Đánh giá trong REPORT.md (Mục B4.1, B5 và B8).
- Commit branch `bao`.

---

### TranThanhNam-2A202603564

**Phần việc phụ trách:** Phần 4 — Xây dựng bộ Eval nhóm & Unit test tool.

**Đóng góp cụ thể:**

- **Đã hoàn thành & có bằng chứng:**
  - Xây dựng bộ đánh giá nhóm [starter_v0/data/eval_group.json](starter_v0/data/eval_group.json) gồm đủ **10 test cases** (5 single-turn: G01–G05 và 5 multi-turn: G06–G10), đạt kết quả đo **10/10 PASS (100%)** trên OpenRouter/gpt-4o-mini ở bản v5-evalfix và v6-date-context.
  - Hoàn thiện các bài unit test trong [starter_v0/tests/test_tools_todo.py](starter_v0/tests/test_tools_todo.py) (bao gồm 6 unit test cho `deduplicate`, test cho `send`, `timeline`, `format`, `policy`, `lookup`, `fetch`), góp phần đưa tổng số test suite lên **210 PASS (0 failed, 0 skipped)** ở môi trường offline/mock.
  - Phát hiện và giữ lại regression test cho các lỗi: `send` nhận giá trị không phải boolean thực thụ, `timeline` lỗi handle có khoảng trắng/@, `paper_text` vi phạm giới hạn ký tự nhỏ.
- **Giới hạn & Việc mở / Tiếp theo (B8):**
  - Bộ group 10 case hiện tại chưa bao phủ trường hợp rẽ nhánh từ chủ đề web sang X mà thiếu handle (khoảng trống này mới chỉ bộc lộ ở phiên chat thực tế).
  - Tiếp tục hoàn thiện thêm các test case hồi quy cho hành vi đa lượt phức tạp và phối hợp review bộ test trên bản tích hợp.

**Bằng chứng đối chiếu:**
- [starter_v0/data/eval_group.json](starter_v0/data/eval_group.json).
- [starter_v0/tests/test_tools_todo.py](starter_v0/tests/test_tools_todo.py), `starter_v0/artifacts/tools_unit_tests.txt`.
- Run JSON: `v5-evalfix_B_group_openrouter_20261110T144452606199.json` và `v6-date-context_B_group_openrouter_20261110T170120261117.json`.
- Báo cáo cá nhân: `report/team/2A202603564_TranThanhNam.md` và commit trên branch `nam`.

---

### NguyenTheCuong-2A202603355

**Phần việc phụ trách:** Phần 5 — Giao diện UI, thu thập Transcript và Tổng hợp báo cáo.

**Đóng góp cụ thể:**

- **Đã hoàn thành & có bằng chứng:**
  - Xây dựng ứng dụng Streamlit `starter_v0/app.py` với giao diện chat, lịch sử hội thoại, xuất transcript JSON và tích hợp hiển thị ngày giờ Việt Nam (UTC+7).
  - Bổ sung cấu hình dependency UI (`streamlit==1.56.0` trong `requirements.txt`).
  - Ghi nhận và lưu trữ các phiên hội thoại thực tế trong thư mục `starter_v0/transcripts/` (bao gồm phiên CLI `v5-evalfix` 3 lượt và phiên Cloud `v6-date-context` 2 lượt).
  - Tổng hợp phần lớn dữ liệu thực nghiệm cho Phần A và Phần B trong [starter_v0/artifacts/REPORT.md](starter_v0/artifacts/REPORT.md), đối chiếu số liệu khớp với các run JSON và `version_log.csv`.
- **Giới hạn & Việc mở / Tiếp theo (B8):**
  - Phiên UI live `v6-date-context` đã hiển thị đúng ngày UTC+7 nhưng thông tin giá vàng/giá xăng vẫn chưa được xác minh đầy đủ về thời điểm hiệu lực và đơn vị từ nguồn tin.
  - Phụ trách tiếp tục rà soát số liệu các đợt eval mới, cập nhật version log và tổng hợp báo cáo nghiệm thu cuối cùng của nhóm.

**Bằng chứng đối chiếu:**
- [starter_v0/app.py](starter_v0/app.py), [starter_v0/requirements.txt](starter_v0/requirements.txt).
- Các file transcript: `ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json`, `v5-evalfix_openrouter_20261110T144638732811.transcript.json`.
- [starter_v0/artifacts/REPORT.md](starter_v0/artifacts/REPORT.md) (Mục B1, B4, B4.1, B5, B8).
- Commit trên branch `cuong`: `0d0d66f`, `66c05a7`.

## Xác nhận bằng chứng trước khi nộp

Các mô tả trên đã được viết đầy đủ theo phân vai, nhưng trạng thái hoàn thành cuối phải được nhóm xác nhận. Trên branch cuong đang kiểm tra, bằng chứng hiện có xác nhận UI/dependency và 8 transcript cũ của Cường. REPORT vẫn là mẫu gốc; chưa có bằng chứng trên branch này để xác nhận toàn bộ phần 1–4 hoặc phiên nghiệm thu mới của bản tích hợp.

| Nội dung cần xác nhận | Người xác nhận | Bằng chứng cần đối chiếu |
|---|---|---|
| Preflight, baseline và các vòng v1–v3 | Ánh | Run JSON, version log, metric và commit thực hiện. |
| Prompt và khai báo tool đã chốt | Trí | Diff, file bàn giao và kết quả trước/sau. |
| Tool mới hoạt động và đăng ký đầy đủ | Bảo | Implementation, TOOL.md, registry/schema và test liên quan. |
| Eval nhóm và pytest đạt tiêu chí | Nam | Case, run JSON, output pytest với số pass/fail/skip thực tế. |
| Demo, transcript và REPORT cuối | Cường | Link/bản triển khai, phiên live đúng version và báo cáo đã tổng hợp. |

