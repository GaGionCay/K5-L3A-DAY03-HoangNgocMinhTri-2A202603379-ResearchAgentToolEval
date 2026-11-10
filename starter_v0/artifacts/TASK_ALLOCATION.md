# Phân công hoàn thiện và bàn giao Research Agent

Team: HoangNgocMinhTri - 2A202603379

Thành viên: Cường, Trí, Ánh, Bảo, Nam

Căn cứ: [REPORT.md](REPORT.md), đặc biệt A1–A3, B1–B6 và [kết quả đối chiếu](artifact_comparison.md).

Đây là phân công công việc tiếp theo và phần thuyết trình. Không dùng bảng này để xác nhận ai đã viết code trước đó. Tên viết tắt được giữ đúng thông tin nhóm cung cấp; chưa tự điền họ tên, mã sinh viên hay tài khoản GitHub còn thiếu.

## Mốc xuất phát đã có bằng chứng

- 11 tool: 10 starter và 1 tool mới `deduplicate`; 210 test offline PASS.
- v6: base 18/20 (90%), group 10/10 (100%), 0 provider_error.
- Hai remote ntc cùng commit 9b3cc29. Prompt/tools local và Cloud khớp sau chuẩn hóa LF/CRLF; hash khác không phải khác chỉ dẫn.
- UI đã nhận đúng 10/11/2026 UTC+7 trong transcript. Tính hiện thời/đơn vị của giá, suy diễn handle từ topic và tiếng Việt trong câu trả lời vẫn cần kiểm chứng/cải thiện.

## Người phụ trách và đầu ra

| Người | Phần REPORT phụ trách | Công việc tiếp theo | File chính / đầu ra bàn giao | Điều kiện hoàn thành |
|---|---|---|---|---|
| **Cường** | B1, B2, B6; tổng hợp báo cáo | Đối chiếu run và version log; phân biệt R03 sai chuỗi query với sai routing, R12 hỏi nội dung với gửi chưa xác nhận; đánh giá khác biệt đường chạy eval/UI; tổng hợp kết quả và review thay đổi của nhóm. | `run_eval.py`, `agent.py`, `versioning.py` nếu cần sửa; bản tổng hợp `REPORT.md`, `version_log.csv`; commit ID và liên kết bằng chứng của từng người. | Metric khớp JSON, không sửa đáp án base để tăng điểm; mô tả đúng giới hạn eval/UI. Nếu thay thuật toán hash phải có version/migration rõ ràng và giữ hash lịch sử. |
| **Trí** | A1–A3; demo UI và B4 | Kiểm tra app Cloud, cấu hình deploy và link demo; chạy kịch bản chat sau khi nhận code đã review; tải transcript, chuẩn bị phần giới thiệu và thao tác demo. | `app.py`; transcript mới trong `transcripts/`; nội dung giới thiệu/demo gửi Cường ghép vào REPORT. | App mở được khi máy cá nhân tắt; ngày Việt Nam đúng; có transcript tương ứng bản triển khai và ghi nhận version/hash. Không đưa API key vào repo. |
| **Ánh** | B2, B4, B6; hành vi hội thoại | Làm rõ hỏi thông tin còn thiếu so với xin xác nhận; không lấy topic web làm account X; trả lời theo ngôn ngữ người dùng. Review `clarify`/`send`: thiếu nội dung thì hỏi nội dung, đã đủ nội dung/đích thì xin xác nhận, chỉ gửi khi được duyệt. | `system_prompt.md`, `chat.py` khi cần; đề xuất case và đoạn phân tích prompt trước/sau. | Kịch bản robotics → xin bài X nhưng thiếu account phải hỏi lại; bổ sung nasa giữ limit; đủ nội dung gửi thì hỏi yes_no. Có test/transcript, không ép hỏi yes_no khi chưa biết nội dung cần gửi. |
| **Bảo** | A2 phần web; B4.1, B5.1 | Kiểm tra `lookup`/`fetch`: ngày hiệu lực của số liệu, ngày xuất bản và giờ truy xuất; xác minh đơn vị/loại giá trước khi trình bày; không khẳng định giá hôm nay nếu chưa đủ nguồn. Phối hợp Ánh về hướng dẫn dùng nguồn. | `tools/lookup/`, `tools/fetch/`; đề xuất thay đổi schema cho Cường review; fixture/test lỗi nguồn cũ và thiếu đơn vị; bằng chứng nguồn không chứa khóa API. | Phân biệt được retrieved_at với as-of; bảng giá cũ có thể còn hiệu lực nhưng phải kiểm tra; thiếu đơn vị/ngày thì hỏi hoặc nêu chưa xác minh, không tự gán VND/chỉ/lượng. |
| **Nam** | B3, B5; QA tools | Kiểm tra regression cho `deduplicate`, X/Twitter, arXiv và policy; thêm group case cho topic→handle, nguồn cũ, thiếu đơn vị và qua nửa đêm; tổ chức chạy test/eval sau khi nhóm chốt code. Không viết lại các test đã đủ chỉ để tăng số lượng. | `tests/`, `data/eval_group.json`; log pytest; run JSON mới và checklist nghiệm thu gửi Cường. | Test có assertion về hành vi, API được mock trong unit test; base giữ nguyên; tách case mới khỏi kết quả group 10 case cũ và ghi rõ denominator; lưu cả FAIL lẫn PASS. |

## Thứ tự phối hợp

1. **Cường chốt mốc hiện tại**: giữ các log v0–v6, ghi commit và kết quả đối chiếu. Mọi người gửi thay đổi để review; không ghi lại toàn bộ công cũ thành đóng góp mới.
2. **Ánh và Bảo xử lý phần còn thiếu** trong phạm vi trên. Cường điều phối nếu cùng sửa `chat.py` hoặc `artifacts/tools.yaml`; mỗi file có một người sửa tại một thời điểm. Nam chuẩn bị case độc lập; Trí chuẩn bị kịch bản demo.
3. **Nam chạy kiểm tra trên bản đã tích hợp**: pytest, base và group với nhãn version mới; ghi rõ model, tổng case, provider_error và run file. Nếu có case FAIL thì giữ bằng chứng và báo nguyên nhân, không coi 100% là điều kiện để báo cáo trung thực.
4. **Trí xác minh trên Cloud sau deploy**: dùng cuộc trò chuyện mới, kiểm tra ngày, web hôm nay, hỏi thiếu account rồi bổ sung nasa, deduplicate; tải transcript. Telegram thật chỉ thử khi nhóm muốn gửi, đã cấu hình và xác nhận nội dung/đích.
5. **Cường cập nhật REPORT/version log và tổng hợp bàn giao** từ đầu ra mọi người. Chủ tài khoản tự commit/push theo phân công; không force push hoặc ghi đè log cũ. README giữ nguyên.

## Checklist bàn giao chung

- [ ] Thay đổi có người review, version/hash và commit được ghi nhận.
- [ ] Có test/regression cho hành vi vừa sửa và kết quả thật từ bản đã tích hợp.
- [ ] Link demo, transcript, run JSON và metric trong REPORT khớp nhau.
- [ ] Phân biệt test mock, model eval và thử live; nêu rõ lỗi còn tồn tại.
- [ ] Cập nhật họ tên đầy đủ/mã sinh viên khi nhóm cung cấp; không tự suy đoán.

Bonus Ollama hoặc thêm nhiều tool chỉ làm khi phần chính đã xong; chưa được đánh dấu hoàn thành khi chưa có bằng chứng.

## Chia phần trình bày

| Người | Nội dung nói/demo |
|---|---|
| Trí | Agent giải quyết việc gì, link demo và một lượt dùng thực tế. |
| Ánh | Prompt, hỏi lại, xác nhận trước gửi và xử lý sửa thông tin giữa các lượt. |
| Bảo | Luồng lookup/fetch, nguồn và cách tránh gọi giá cũ là giá hôm nay. |
| Nam | Tool mới deduplicate, test contract/regression và bộ group. |
| Cường | Quá trình v0→v6, số liệu, lỗi còn lại, giới hạn và kết luận kỹ thuật. |
