# Báo cáo cá nhân — HoangNgocMinhTri-2A202603379

## 1. Thông tin thành viên

- **Họ và tên:** Hoàng Ngọc Minh Trí
- **MSSV:** 2A202603379
- **Email:** minhtrihoangngoc@gmail.com
- **Lớp:** L3A
- **Tài khoản GitHub:** [GaGionCay](https://github.com/GaGionCay)
- **Repository chung:** [GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval)
- **Branch cá nhân:** `hmt`
- **Bài tập:** Day 03 — Prompt Engineering & Tool Calling, Research Agent Tool Eval

---

## 2. Phần việc phụ trách

Trong đề tài nghiên cứu và phát triển Research Agent Tool Eval của nhóm, tôi đảm nhận vai trò **Phần 2 — Prompt Engineering, Khai báo Tool Schema, Cơ chế Ranh giới An toàn (Guardrails) & Triển khai Demo Cloud**.

Các nhiệm vụ trọng tâm được giao bao gồm:
1. **Thiết kế & Tối ưu System Prompt (`artifacts/system_prompt.md`)**: Xây dựng bộ quy tắc điều hướng (routing rules) công cụ, quy tắc hỏi lại khi thiếu thông tin (`clarify`), giữ ngữ cảnh đa lượt (multi-turn), xử lý chuyển đổi nguồn (web ↔ X/Twitter), và định tuyến chính xác nhóm công cụ mở rộng (Bonus Tools).
2. **Đồng bộ hóa Khai báo Tool Schema (`artifacts/tools.yaml`)**: Chuẩn hóa định nghĩa schema các công cụ, rà soát tính hợp lệ kiểu dữ liệu tham số, mô tả chi tiết từng đối số để LLM sinh tool call đúng format.
3. **Cơ chế An toàn 2 bước cho thao tác Gửi (`send` & `clarify`)**: Thiết kế luồng chặn agent tự ý gửi tin/bài khi chưa có xác nhận rõ ràng từ người dùng; bắt buộc gọi `clarify` dạng `yes_no` hiển thị đầy đủ `draft` nội dung và `destination` trước khi cho phép set `confirmed=True`. Viết bộ test kiểm thử luồng an toàn (`test_send_confirmation_flow.py`).
4. **Triển khai Streamlit Cloud Demo & Thực nghiệm Live Transcript**: Đóng gói và triển khai ứng dụng Research Agent lên Streamlit Cloud phục vụ trải nghiệm công khai; thực hiện các phiên tương tác live và xuất transcript minh chứng luồng hoạt động.

---

## 3. Đóng góp cụ thể

### 3.1. Thiết kế và hoàn thiện System Prompt (`starter_v0/artifacts/system_prompt.md`)
- **Quy tắc điều hướng công cụ lõi**:
  - Hướng dẫn LLM phân biệt rõ ràng giữa tìm kiếm web chung (`lookup`), tra cứu tin tức thời sự (`lookup` với `topic="news"`, `timeframe="day"`), tìm kiếm bài đăng theo từ khóa trên X/Twitter (`social_search`), và lấy bài đăng theo tài khoản cụ thể (`timeline`).
  - Xử lý tình huống người dùng yêu cầu tổng hợp đa nguồn (cả web lẫn tweet) bằng cách gọi đồng thời cả `lookup` và `social_search`.
  - Duy trì ngữ cảnh yêu cầu, ràng buộc thời gian và chủ đề qua các lượt hội thoại kế tiếp; cập nhật kịp thời khi người dùng đính chính.
- **Định tuyến nhóm công cụ mở rộng (Bonus Tools Routing)**:
  - Bổ sung quy tắc định tuyến chi tiết cho 5 bonus tools nhằm tránh việc mô hình gọi nhầm sang tool web thông thường:
    - `policy`: Tra cứu chính sách nội bộ, hướng dẫn tuân thủ, quy định bản quyền, AI usage.
    - `papers`: Tìm kiếm bài báo khoa học, preprint (arXiv) theo chủ đề/từ khóa.
    - `paper_text`: Đọc và trích xuất toàn văn bài báo học thuật theo arXiv paper ID hoặc URL.
    - `format`: Định dạng và cấu trúc hóa báo cáo nghiên cứu, digest hoặc template markdown.
    - `deduplicate`: Lọc bỏ các bài viết/bản tin trùng lặp khỏi tập dữ liệu thu thập.

### 3.2. Cơ chế Ranh giới An toàn 2 bước (Two-Step Confirmation Guardrail)
- **Quy trình bảo vệ hành động gửi**:
  - Chặn triệt để hành vi mô hình tự kích hoạt `send` ở lượt đầu tiên khi chưa có xác nhận.
  - **Bước 1**: Thu thập đầy đủ `draft` nội dung và địa chỉ gửi `destination`. Nếu thiếu, gọi `clarify(response_type="text")` để hỏi lại, tuyệt đối không tự bịa thông tin.
  - **Bước 2**: Hiển thị bản nháp hoàn chỉnh và đích đến, sau đó gọi `clarify(response_type="yes_no")` kèm tham số `draft` và `destination`. Chỉ khi người dùng đồng ý (`yes`/xác nhận rõ ràng ở lượt sau), tham số `confirmed` mới được đặt thành `true` để gọi `send`.
- **Cài đặt & Kiểm thử code**:
  - Cập nhật logic điều hướng và kiểm tra trạng thái trong `starter_v0/chat.py` và `starter_v0/tools/send/tool.py`.
  - Xây dựng file unit test chuyên biệt `starter_v0/tests/test_send_confirmation_flow.py` (187 dòng code) bao phủ toàn bộ các tình huống: từ chối khi thiếu draft, từ chối khi thiếu destination, xác nhận hợp lệ, hủy bỏ khi người dùng từ chối (`no`).

### 3.3. Chuẩn hóa Schema và Registry Tool (`starter_v0/artifacts/tools.yaml` & `tools/__init__.py`)
- Rà soát toàn bộ các khai báo trong `tools.yaml`, bảo đảm khớp 100% với signature thực tế trong `tools/`:
  - Đồng bộ `papers` và alias `arxiv_search` để tránh lỗi lệch registry giữa schema khai báo và hàm thực thi.
  - Chuẩn hóa các trường enum, type, description của `clarify`, `lookup`, `fetch`, `social_search`, `timeline`, `send`.
  - Khắc phục triệt để lỗi kiểu dữ liệu đối số (như `limit` kiểu int, boolean flags cho confirmation).

### 3.4. Triển khai Streamlit Cloud và Tạo Live Transcript
- Cấu hình và đưa ứng dụng lên **Streamlit Cloud**: [https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app](https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app).
- Trực tiếp tương tác và ghi lại phiên live minh chứng luồng an toàn `send`:
  - File: `starter_v0/transcripts/live_send_confirmation.transcript.json`.
  - Lượt 1: Yêu cầu gửi bài -> Agent dừng, hiển thị preview và gọi `clarify(response_type="yes_no")`.
  - Lượt 2: Người dùng xác nhận "yes" -> Agent gọi `send(confirmed=true)`.

---

## 4. Bằng chứng đối chiếu

### 4.1. File và Commit trên Git
- **Nhánh thực hiện:** `hmt` (đã merge vào `main` tại commit `1e7ca40`, `ca9cfdb`, `f0e4451`).
- **Các commit tiêu biểu của tôi:**
  - `7b4ff28` — *Feat: Completed assignment by Hoang Ngoc Minh Tri*: Tích hợp logic an toàn send confirmation, cập nhật system prompt, bổ sung test flow, đồng bộ schema.
  - `62f7eb3` — *Feat:Update code by HoangNgocMinhTri*: Hoàn thiện các hàm định tuyến trong `chat.py`, `tools.yaml`, và `system_prompt.md`.
  - `d7cc654` — *fix(test): move __future__ annotations import to top of test_tools_todo.py*.
  - `f0e4451` — *docs: sync TEAM.md, clarify v4 gap in REPORT.md, and add live send transcript*.
- **Các file trực tiếp đóng góp/chỉnh sửa:**
  - `starter_v0/artifacts/system_prompt.md`
  - `starter_v0/artifacts/tools.yaml`
  - `starter_v0/chat.py`
  - `starter_v0/tools/clarify/tool.py` & `TOOL.md`
  - `starter_v0/tools/send/tool.py` & `TOOL.md`
  - `starter_v0/tests/test_send_confirmation_flow.py`
  - `starter_v0/transcripts/live_send_confirmation.transcript.json`

### 4.2. Kết quả Đánh giá và Kiểm thử
- **Đánh giá Eval (Model: OpenRouter / gpt-4o-mini):**
  - Đóng góp vào việc cải thiện độ chính xác từ `v0` (baseline) lên `v3` (17/20 - 85%), `v5-tools-complete` (19/20 - 95%), và đạt **10/10 PASS (100%)** ở bộ test nhóm `eval_group.json` (bản `v5-evalfix` và `v6-date-context`).
- **Unit Test suite:**
  - Bộ test xác nhận gửi (`test_send_confirmation_flow.py`) đạt 100% passed.
  - Toàn bộ suite bài tập chạy qua pytest: **210 PASS (0 failed, 0 skipped)** ở chế độ mock/offline.

### 4.3. Ứng dụng & Dịch vụ Trực tuyến
- **Web App Demo:** [Streamlit Cloud Research Agent](https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app).

---

## 5. Tự đánh giá

### 5.1. Những việc đã làm tốt
- Xây dựng được bộ System Prompt chặt chẽ, ngăn ngừa hiệu quả các lỗi phổ biến của LLM như tự bịa đặt tham số (hallucination) hoặc gọi nhầm công cụ.
- Thiết lập thành công ranh giới an toàn cho hành động gửi (`send`), biến luồng tương tác nguy hiểm thành quy trình 2 bước có kiểm soát chặt chẽ.
- Hoàn thành đầy đủ các file cấu hình schema `tools.yaml` đồng bộ với code thực thi, không để xảy ra lỗi mismatch khi chạy eval.
- Vận hành ổn định ứng dụng Streamlit trên Cloud phục vụ kiểm thử thực tế.

### 5.2. Giới hạn tồn tại và Hướng khắc phục (Đồng bộ Mục B8 của REPORT.md)
- **Hành vi rẽ nhánh Web sang X/Twitter:** Khi người dùng đang thảo luận về một chủ đề trên web (ví dụ: `robotics`) rồi ở lượt kế tiếp yêu cầu "lấy bài đăng mới nhất trên X", prompt đôi khi vẫn chưa ngăn được LLM tự suy diễn chủ đề `robotics` thành account handle (`screenname="robotics"`) thay vì chủ động gọi `clarify` để hỏi tên tài khoản cụ thể.
- **Hướng khắc phục tiếp theo:** Bổ sung thêm một điều khoản rõ ràng trong `system_prompt.md` quy định: *"Khi chuyển từ tìm kiếm web sang tra cứu bài đăng theo tài khoản trên X, nếu người dùng chưa chỉ định rõ tài khoản bắt đầu bằng @ hoặc tên profile cụ thể, bắt buộc phải gọi clarify để hỏi rõ account handle, không được lấy từ khóa web làm screenname"*.

### 5.3. Mức độ hoàn thành & Tự chấm điểm
- **Mức độ hoàn thành:** 100% khối lượng công việc được phân công theo phân vai nhóm.
- **Tự chấm điểm:** 10/10.
