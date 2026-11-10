# Báo cáo cá nhân — HoVaTen-MSSV

## 1. Thông tin thành viên

- Họ tên: Hoàng Văn Bảo
- MSSV: 2A202603549
- Email: 26ai.baohv@vinuni.edu.vn

## 2. Phần việc phụ trách

Vai trò: **Người 3 – Phát triển tool**.

Nhiệm vụ được giao: chọn và triển khai ít nhất một tool mới; viết `tool.py` và `TOOL.md`; đăng ký tool trong `tools/__init__.py` và `tools.yaml`; sửa bug trong tool nếu phát hiện.

Tool phụ trách: **`lookup`** và **`fetch`** (nhánh `bao`).

## 3. Đóng góp cụ thể

- **`tools/lookup/`**: cập nhật `tool.py` (hàm `web_search`) và `TOOL.md`. [Mô tả: tool tìm gì, nhận tham số nào, trả về gì.]
- **`tools/fetch/`**: cập nhật `tool.py` và `TOOL.md`. [Mô tả: tool lấy dữ liệu từ đâu, xử lý lỗi/timeout ra sao.]
- **Đăng ký tool**: khai báo `lookup` và `fetch` trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml`; tên, mô tả, tham số khớp với `tool.py`.
- **Bug đã phát hiện và sửa**: [ghi rõ bug, nguyên nhân, cách sửa; nếu không có bug thì ghi "không phát hiện bug"].
- **Kiểm thử**: [ghi các test đã chạy và kết quả, ví dụ `pytest starter_v0/tests -v`: X passed, Y failed].

## 4. Bằng chứng

- File/commit/PR:
  - Nhánh: `bao` (repo `GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval`)
  - Commit `2196d38` – "update tools lookup và fetch": `tools/fetch/tool.py`, `tools/fetch/TOOL.md`, `tools/lookup/tool.py`, `tools/lookup/TOOL.md` (118 dòng thêm, 24 dòng xóa)
  - Commit `6d99f5c` – "register lookup and fetch tools": `tools/__init__.py`, `artifacts/tools.yaml`, `tools/lookup/TOOL.md` (279 dòng thêm, 81 dòng xóa)
  - PR: [link PR nếu có]
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude để hướng dẫn thao tác Git (chuyển nhánh, add chọn lọc, commit, push) và đối chiếu yêu cầu nhiệm vụ. [Ghi thêm nếu dùng AI để viết/sửa code tool.]
  - Tự kiểm tra bằng `git status` trước mỗi commit (chỉ add đúng file thuộc phần mình), đọc output `git push` để xác nhận commit lên nhánh `bao`, và [chạy `python -c "import starter_v0.tools"` và `pytest` để xác nhận tool import và chạy được].

## 5. Tự đánh giá

- **Làm được**: hoàn thiện hai tool `lookup` và `fetch` (code và hướng dẫn), đăng ký đủ ở `tools/__init__.py` và `tools.yaml`, đã push lên nhánh `bao`.
- **Hạn chế**: chưa có unit test riêng cho tool, còn cảnh báo (problems) trong `lookup/tool.py` và `fetch/tool.py`, import `deduplicate` trong `tools/__init__.py` cần kiểm tra khi gộp nhánh.
- **Cần cải thiện**: bổ sung test, xử lý lỗi mạng chặt hơn, thống nhất tên tool với `tools.yaml` khi merge các nhánh.
- **Tự chấm**: [9/10] .
