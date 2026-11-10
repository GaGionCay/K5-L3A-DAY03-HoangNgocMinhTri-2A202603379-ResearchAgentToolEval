# Báo cáo cá nhân — Nguyễn Thế Cường - 2A202603355

## 1. Thông tin thành viên

- **Họ tên:** Nguyễn Thế Cường
- **MSSV:** 2A202603355
- **Email:** [ntcuong1113@gmail.com](mailto:ntcuong1113@gmail.com)
- **GitHub:** [Chill2004](https://github.com/Chill2004)
- **Vai trò:** Demo & Báo cáo — thành viên phụ trách Phần 5

## 2. Phần việc phụ trách

Phụ trách chuẩn bị giao diện dùng thử cho research agent, tổ chức các lượt chat demo, lưu bằng chứng hội thoại và tổng hợp báo cáo từ kết quả của nhóm. Các đầu việc chính gồm:

- Xây dựng và chạy giao diện Streamlit trong `starter_v0/app.py`.
- Chuẩn bị link demo và câu hỏi mẫu để nhóm khác có thể dùng thử.
- Thực hiện ít nhất 3 lượt chat live, quan sát cách agent gọi tool và lưu transcript.
- Chuẩn bị Phần A giới thiệu agent trước demo; tổng hợp Phần B sau khi nhận kết quả từ các thành viên.
- Đối chiếu nội dung báo cáo với file, phiên bản và log thực tế.

## 3. Đóng góp cụ thể

### 3.1. Xây dựng giao diện và chuẩn bị demo

- Chuẩn bị UI Streamlit với ô nhập yêu cầu, lịch sử hội thoại, nút **Cuộc trò chuyện mới** và **Tải transcript**.
- Bổ sung dependency Streamlit trong `starter_v0/requirements.txt` để chạy giao diện.
- Hiển thị ngày Việt Nam UTC+7 và lưu thông tin thời gian trong transcript.
- Điều chỉnh UI để dùng context ngày giờ chung khi chạy với bản v6, đồng thời vẫn hoạt động với starter chưa có phần xử lý này.
- Chuẩn bị các câu hỏi mẫu về tìm tin web, lấy bài đăng X/Twitter, đọc URL và hỏi thông tin còn thiếu.
- Đã dùng và deploy lên web [link Streamlit Cloud](https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app)

### 3.2. Thực hiện chat live và lưu transcript

- Phiên CLI `v5-evalfix` có **3 lượt live**: tìm tin robotics trên web, yêu cầu lấy bài đăng X khi chưa có tài khoản, rồi bổ sung tài khoản nasa.
- Rà soát các lượt hội thoại để kiểm tra cách agent xử lý yêu cầu thiếu thông tin và phản hồi khi người dùng bổ sung tài khoản.
- Ở lượt bổ sung nasa, agent đổi tài khoản và giữ `limit=2` từ yêu cầu trước.
- Phiên UI `v6-date-context` có **2 lượt thử**, ghi nhận ngày **10/11/2026, UTC+7** đúng; thời điểm áp dụng và đơn vị của giá vẫn chưa được xác minh đầy đủ.
- Lưu transcript kèm thông tin phiên bản để nhóm có thể xem lại và đối chiếu kết quả demo.

### 3.3. Kiểm tra UI và tổng hợp báo cáo

- Kiểm tra UI offline bằng Streamlit AppTest với provider/tool mô phỏng: ba lượt hội thoại, hỏi lại, giữ lịch sử, xử lý UTC+7, tải transcript và tạo phiên mới.
- Kiểm tra trên cả starter và bản v6 tích hợp; UI không chèn trùng context ngày giờ. Các lần kiểm tra này không gọi API thật và không thay thế chat live.
- Chuẩn bị nội dung giới thiệu, danh sách chức năng và kịch bản demo để phục vụ Phần A.
- Đối chiếu transcript, run log và kết quả của nhóm khi tổng hợp Phần B; bản báo cáo cuối vẫn cần nhóm xác nhận.

Lệnh chạy giao diện từ thư mục gốc repository:

```powershell
cd starter_v0
python -m streamlit run app.py
```

Sau khi chạy, mở `http://localhost:8501`, tạo cuộc trò chuyện mới và tải transcript sau phiên thử. Chỉ ghi kết quả đã quan sát được vào báo cáo.

## 4. Bằng chứng

- **Code UI và dependency:** [starter_v0/app.py](../../starter_v0/app.py), [starter_v0/requirements.txt](../../starter_v0/requirements.txt).
- **Transcript CLI 3 lượt:** [v5-evalfix_openrouter_20261110T144638732811.transcript.json](../../starter_v0/transcripts/v5-evalfix_openrouter_20261110T144638732811.transcript.json).
- **Transcript UI 2 lượt:** [ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json](../../starter_v0/transcripts/ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json).
- **Commit trên branch cuong:** [343abac](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval/commit/343abace8f838b0768a73c84aff75cb06c10dcd8) đưa UI, dependency và 8 transcript lên nhánh; [a619b44](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval/commit/a619b44ae5ef08c1ece65d0ef1c4156053ebc067) cập nhật riêng app.py để tương thích starter và bản v6.
- **AI/công cụ đã dùng:** ChatGPT/Codex hỗ trợ viết và chỉnh UI, đọc lỗi, soạn nội dung demo và báo cáo; Streamlit chạy giao diện, AppTest kiểm tra luồng UI offline.
- **Cách kiểm tra kết quả:** xem lại diff, file trong commit, tool call, tham số và câu trả lời trong transcript. Phân biệt kết quả mô phỏng với API thật; không coi trạng thái answered là bằng chứng agent đã hiểu đúng yêu cầu.

## 5. Tự đánh giá

- Qua phần việc này, mình hiểu rõ hơn cách đưa agent từ dòng lệnh lên giao diện để người khác dùng thử và cách lưu bằng chứng cho từng phiên hội thoại.
- Mình nhận ra ngoài việc kiểm tra giao diện, còn cần đối chiếu yêu cầu của người dùng với tool call, tham số và câu trả lời để đánh giá kết quả demo.
- Việc thử ngày giờ giúp mình phân biệt ngày hiện tại với thời điểm của dữ liệu trong nguồn. Hiển thị đúng UTC+7 chưa đủ để khẳng định giá trả về là giá mới nhất.
- Phần còn cần hoàn thành là xác nhận link chạy đúng bản tích hợp cuối, thử lại ít nhất 3 lượt live trên bản đó và nhận đủ kết quả nhóm để chốt báo cáo.
