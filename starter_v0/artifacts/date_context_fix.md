# v6-date-context — ngày hiện tại và độ mới của nguồn

## Nguyên nhân đã xác nhận trong code

- Vòng chat trước đây không đưa đồng hồ/ngày hiện tại cho model.
- lookup mặc định timeframe=week; một query giá “hôm nay” có thể nhận nguồn trong tuần.
- Mapping bỏ published_date dù nhà cung cấp có trả, làm model thiếu tín hiệu thời gian.
- Chưa có transcript Cloud của lượt lỗi để kết luận chính xác query, timeframe hay nguồn gây ra câu trả lời 07/11.

## Thay đổi

- time_context.py: tính ngày hiện tại bằng UTC+7, không hard-code ngày 10/11. Có test đổi ngày/tháng/năm.
- chat.py: thêm system context cho mỗi lượt và giữ runtime_context trong cả answered/waiting/max-rounds.
- app.py: nhãn v6-date-context và hiển thị ngày Việt Nam từ đồng hồ máy chủ.
- lookup: mặc định không lọc ngày xuất bản; có max_age_hours 0-720, giữ published_date và retrieved_at riêng biệt.
- time_range là bộ lọc theo ngày xuất bản; các trang giá/thời tiết có thể cập nhật nội dung nhưng giữ ngày xuất bản cũ. max_age_hours=0 yêu cầu lấy trang live, không tự chứng minh thời điểm của con số trong nội dung.
- Model được yêu cầu nêu rõ chưa xác minh khi nguồn cũ/thiếu thời điểm, không đổi nhãn giá cũ thành giá hôm nay.

## Xác minh

- 210 test PASS, 0 FAIL, 0 SKIP (175 + 9 + 26), offline.
- Đã có transcript Cloud hỏi giá vàng và ngày/giá xăng, nhưng chưa đối chiếu để xác minh giá và đơn vị. Đã có run v6 base 18/20 (90%) và group 10/10 (100%), 0 provider_error.
- Hai run dùng ResearchAgent.run, không qua vòng chat/UI có runtime date context; không dùng điểm này để khẳng định lỗi ngày/giá trên Cloud đã hết.
- Base FAIL R03 do query khác chuỗi đáp án, R12 do clarify(text) thay vì yes_no; chi tiết và liên kết run ở REPORT B1/B2.
- Các run v0–v5 và transcript lịch sử giữ nguyên. Không sửa README và không commit/push.
- App Cloud đang lấy code từ fork chill2004/… branch ntc theo log triển khai; cập nhật riêng repo GaGionCay không tự cập nhật fork.

## Kiểm tra sau deploy

1. Bấm Cuộc trò chuyện mới; kiểm tra dòng ngày Việt Nam trên UI.
2. Hỏi “Hôm nay là ngày nào theo giờ Việt Nam?”; đối chiếu với đồng hồ thực tế.
3. Hỏi giá hôm nay; tải transcript và kiểm tra runtime_context, lookup query và max_age_hours, ngày nguồn và nội dung as-of. Nếu không xác minh được nguồn mới, câu trả lời phải nêu rõ giới hạn.
4. Hai run eval v6 đã được ghi ở REPORT/version_log. Giữ riêng bằng chứng live ngày giờ trên Cloud; không sửa kết quả cũ.

Nguồn kỹ thuật: https://docs.tavily.com/documentation/api-reference/endpoint/search

## Transcript Cloud bổ sung

- Bằng chứng: [transcript 2 lượt](../transcripts/ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json); giữ nguyên bytes file tải về.
- Runtime context đúng 2026-11-10 UTC+7 ở cả hai lượt; lượt 2 trả lời đúng ngày. Đây là bằng chứng cho đồng hồ/ngày, chưa phải độ đúng giá.
- Vàng: max_age_hours=0, query không có ngày cụ thể; snippet PNJ/BTMC thiếu ngày/đơn vị rõ ràng, câu trả lời vẫn gán VNĐ và gọi “hôm nay”. Chưa đạt kiểm chứng thời điểm/đơn vị.
- Xăng: không truyền max_age_hours; bảng nguồn có hiệu lực từ 05/11, trang hiển thị 07/11. Chưa kiểm tra còn hiệu lực 10/11. Không khẳng định giá sai chỉ vì ngày áp dụng trước đó.
- Đã đối chiếu: hash Cloud `pc5fd2628fcf2+t190818f266ea` trùng hash local sau chuẩn hóa CRLF→LF. Prompt/tools khớp nội dung; hai remote ntc cùng commit 9b3cc29 tại lúc kiểm tra. Hash khác do versioning.py tính bytes, không phải bằng chứng khác chỉ dẫn. Điểm eval vẫn không phải điểm phiên UI vì khác đường chạy. Xem [artifact_comparison.md](artifact_comparison.md).
- Bước tiếp: xử lý ngày hiệu lực cùng đơn vị từ nội dung nguồn theo [TASK_ALLOCATION.md](TASK_ALLOCATION.md), rồi lưu transcript mới. Chưa sửa thêm code trong lần bổ sung bằng chứng này.
