# Báo cáo cá nhân — NguyenTheCuong-2A202603355

## 1. Thông tin thành viên

- Họ tên: Nguyễn Thế Cường.
- MSSV: 2A202603355.
- Email: ntcuong1113@gmail.com.
- Lớp: L3A.
- GitHub: [Chill2004](https://github.com/Chill2004).
- Bài tập: Day 03 — Research Agent Tool Eval.
- Repository nhóm: [GaGionCay/ResearchAgentToolEval](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval).
- Nhánh cá nhân: [cuong](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval/tree/cuong).

## 2. Phần việc phụ trách

Tôi phụ trách **Phần 5 — Demo và báo cáo**. Công việc gồm chuẩn bị giao diện dùng thử, link demo, thực hiện hội thoại live và lưu transcript, sau đó tổng hợp nội dung giới thiệu cùng kết quả của nhóm vào báo cáo.

Theo phân vai đã thống nhất, Ánh phụ trách đánh giá và quản lý phiên bản; Trí phụ trách prompt và khai báo tool; Bảo phát triển tool; Nam phụ trách eval và unit test. Phần của tôi tập trung vào cách dùng agent, trải nghiệm demo và bằng chứng hội thoại. Kết quả đánh giá, code tool và test của các phần khác được dùng làm đầu vào khi tổng hợp, không ghi thành đóng góp cá nhân của tôi.

## 3. Đóng góp cụ thể

### Chuẩn bị giao diện Streamlit

Tôi chuẩn bị giao diện trong `starter_v0/app.py` để người dùng có thể thử agent qua ô chat. Giao diện hiển thị lịch sử hội thoại, có nút **Cuộc trò chuyện mới** và **Tải transcript**. Dependency Streamlit được bổ sung trong requirements.txt để có thể chạy lại giao diện.

UI có dòng ngày Việt Nam UTC+7 và lưu thông tin thời gian trong transcript. Khi ghép với bản v6, UI dùng context ngày giờ từ vòng chat chung. Khi chạy với starter chưa có phần này, UI cung cấp context ngày giờ riêng. Cách xử lý đó giúp branch cá nhân vẫn chạy được mà không phải đưa kèm toàn bộ thay đổi prompt/tool/test của nhóm.

Lệnh chạy UI từ thư mục gốc repository:

```powershell
cd starter_v0
python -m streamlit run app.py
```

Sau đó mở `http://localhost:8501`.

### Chuẩn bị nội dung và luồng demo

Tôi chuẩn bị phần giới thiệu ngắn về agent, danh sách chức năng và các câu hỏi mẫu: tìm tin web, lấy bài đăng theo tài khoản, đọc URL và thử tình huống thiếu thông tin. Luồng demo đi từ một yêu cầu đầy đủ đến một yêu cầu cần hỏi lại để người xem thấy cách agent xử lý hội thoại nhiều lượt.

Ở giai đoạn thử trước, nhóm đã dùng [link Streamlit Cloud](https://k5-l3a-day03-hoangngocminhtri-2a202603379-researchagenttooleva.streamlit.app). Link này là bằng chứng về bản demo đã sử dụng; chưa xác nhận bản đang triển khai được lấy từ branch cuong mới nhất.

### Lưu và xem lại transcript thực tế

Tôi đưa 8 transcript đã có từ ntc sang branch cuong, giữ nguyên phiên bản và nội dung gốc. Trong đó, phiên CLI `v5-evalfix` có 3 lượt live:

| Lượt | Yêu cầu của người dùng | Tool call thực tế | Nhận xét |
|---|---|---|---|
| 1 | Tìm 3 tin tức về robotics trên web trong tuần này, kèm nguồn. | `lookup` với query robotics, topic news, timeframe week và max_results 3. | Agent chọn đúng nguồn web và tham số; câu trả lời có liên kết. Chưa kiểm chứng thủ công từng bài gốc. |
| 2 | Lấy 2 bài đăng mới nhất trên X giúp tôi. | `timeline` với screenname robotics và limit 2. | Chưa đúng: agent lấy chủ đề trước làm tên tài khoản thay vì hỏi lại. |
| 3 | Tài khoản nasa. | `timeline` với screenname nasa và limit 2. | Agent tiếp nhận tài khoản được sửa và giữ số lượng từ lượt trước. |

Phiên UI `v6-date-context` có thêm 2 lượt thử về giá vàng, ngày hiện tại và giá xăng. Runtime context ghi đúng **10/11/2026, UTC+7** và lượt hỏi ngày được trả lời đúng. Tuy nhiên, thời điểm áp dụng và đơn vị của giá vẫn chưa được xác minh đầy đủ. Tôi giữ nhận xét này trong phần bằng chứng thay vì coi mọi lượt có trạng thái answered là thành công.

Các phiên trên là bằng chứng đã có trước khi tách branch; tôi không đổi nhãn để coi chúng là những lần thử mới của bản UI hiện tại.

### Kiểm tra UI và chuẩn bị báo cáo

UI được kiểm tra offline bằng Streamlit AppTest với provider và tool mô phỏng. Kịch bản kiểm tra gồm ba lượt tìm tin, hỏi lại tài khoản và tiếp nhận nasa; đồng thời kiểm tra lịch sử, limit=2, context UTC+7, nút tải transcript và tạo phiên mới. Cả bản starter và bản v6 tích hợp đều qua kiểm tra này, không chèn trùng context ngày giờ.

Tôi dùng ChatGPT/Codex hỗ trợ chuẩn bị nội dung giới thiệu và đối chiếu báo cáo với transcript, run log. Nội dung tổng hợp v6 hiện có trong working tree để nhóm tham khảo. Hai commit cá nhân đã push chỉ chứa UI, dependency và transcript như liệt kê dưới đây; chưa bao gồm báo cáo nhóm cuối hay toàn bộ code tích hợp.

## 4. Bằng chứng

### File và commit

| Bằng chứng | Nội dung có thể đối chiếu |
|---|---|
| [starter_v0/app.py](../../starter_v0/app.py) | Giao diện chat, tạo phiên mới, tải transcript và xử lý context ngày giờ. |
| [starter_v0/requirements.txt](../../starter_v0/requirements.txt) | Dependency Streamlit dành cho UI. |
| [Thư mục transcript](../../starter_v0/transcripts) | 8 transcript giữ nguyên phiên bản và kết quả cũ. |
| [CLI v5-evalfix — 3 lượt](../../starter_v0/transcripts/v5-evalfix_openrouter_20261110T144638732811.transcript.json) | Phiên live tìm tin, thiếu account và sửa sang nasa; có lỗi ở lượt 2. |
| [UI v6-date-context — 2 lượt](../../starter_v0/transcripts/ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json) | Context ngày đúng, cùng giới hạn khi trả lời giá hiện tại. |
| [Commit 343abac](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval/commit/343abace8f838b0768a73c84aff75cb06c10dcd8) | Đưa app.py, dependency UI và 8 transcript lên branch cuong. |
| [Commit a619b44](https://github.com/GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval/commit/a619b44ae5ef08c1ece65d0ef1c4156053ebc067) | Chỉ cập nhật app.py để tương thích starter và bản v6. |

Báo cáo nhóm theo cấu trúc nộp bài nằm ở `report/team/group_report.md`; nhóm cần chốt nội dung và bản tích hợp trước khi nộp cuối. Các ghi nhận kỹ thuật v6 hiện có trong `starter_v0/artifacts/REPORT.md` ở working tree không tự đồng nghĩa đã nằm trong commit nộp của nhóm.

### AI/công cụ đã dùng và cách kiểm tra kết quả

| Công cụ | Mục đích sử dụng | Cách kiểm tra |
|---|---|---|
| ChatGPT/Codex | Hỗ trợ viết/chỉnh UI, đọc lỗi, đối chiếu file và soạn báo cáo. | Xem lại diff, kiểm tra file thuộc Phần 5, đối chiếu nội dung với commit và transcript thực tế. |
| Streamlit và AppTest | Chạy giao diện và kiểm tra luồng UI offline. | Dùng provider/tool mô phỏng để kiểm tra ba lượt, lịch sử, hỏi lại, UTC+7, tải transcript và tạo phiên mới; không gọi API thật hoặc ghi thành transcript live. |
| Transcript JSON | Xem agent đã gọi tool và trả lời như thế nào. | Đọc user request, tool call, tham số, dữ liệu trả về và version/hash; ghi rõ lỗi hoặc giới hạn còn lại. |

Không dùng câu trả lời do AI soạn hoặc kết quả mock để khẳng định model/API thật đã hoạt động đúng. Các điểm eval trong báo cáo nhóm cần dẫn đúng run tương ứng và do người phụ trách xác nhận.

## 5. Tự đánh giá

Tôi đã có phần UI và bằng chứng hội thoại để nhóm dùng khi chuẩn bị demo. Hai commit trên branch cuong giúp tách phần giao diện khỏi prompt, code tool và test do các thành viên khác phụ trách. Tôi cũng nhận ra cần kiểm tra nội dung thực tế: agent có thể lấy được dữ liệu nhưng vẫn hiểu sai yêu cầu, như việc lấy chủ đề robotics làm tên tài khoản X.

Việc thử ngày giờ cho thấy trả lời đúng ngày và trả về dữ liệu mới là hai yêu cầu khác nhau. Dòng UTC+7 trên giao diện giúp xác định ngày hiện tại, nhưng giá trong nguồn vẫn cần kiểm tra thời điểm áp dụng và đơn vị. Đây là điểm tôi cần chú ý khi trình bày demo để không giới thiệu quá khả năng đã kiểm chứng.

Phần còn cần hoàn thành là xác nhận link chạy đúng bản nhóm chốt, thử lại ít nhất ba lượt live trên bản đó và nhận đủ kết quả từ Ánh, Trí, Bảo, Nam để hoàn thiện báo cáo chung. Tôi chưa coi kiểm tra offline hoặc transcript cũ là bằng chứng nghiệm thu mới cho bản tích hợp cuối.
