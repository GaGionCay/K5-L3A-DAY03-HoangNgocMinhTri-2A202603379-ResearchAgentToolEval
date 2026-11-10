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
- Chưa gọi live API để xác minh giá vàng, chưa chạy lại base/group cho v6.
- Các run v0–v5 và transcript lịch sử giữ nguyên. Không sửa README và không commit/push.
- App Cloud đang lấy code từ fork chill2004/… branch ntc theo log triển khai; cập nhật riêng repo GaGionCay không tự cập nhật fork.

## Kiểm tra sau deploy

1. Bấm Cuộc trò chuyện mới; kiểm tra dòng ngày Việt Nam trên UI.
2. Hỏi “Hôm nay là ngày nào theo giờ Việt Nam?”; đối chiếu với đồng hồ thực tế.
3. Hỏi giá hôm nay; tải transcript và kiểm tra runtime_context, lookup query và max_age_hours, ngày nguồn và nội dung as-of. Nếu không xác minh được nguồn mới, câu trả lời phải nêu rõ giới hạn.
4. Chạy lại eval với nhãn v6-date-context trước khi cập nhật bảng metric.

Nguồn kỹ thuật: https://docs.tavily.com/documentation/api-reference/endpoint/search
