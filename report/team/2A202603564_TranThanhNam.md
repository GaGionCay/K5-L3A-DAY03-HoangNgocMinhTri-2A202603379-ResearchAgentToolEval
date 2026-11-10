# Báo cáo cá nhân

## 1\. Thông tin thành viên

* **Họ tên:** Trần Thành Nam
* **MSSV:** 2A202603564
* **Email:** thanhnam120304@gmail.com
* **Nhóm / dự án:** Research Agent Tool Eval — Day 03 Lab v2
* **Vai trò:** Eval \& Unit Test (thành viên phụ trách kiểm thử)

## 2\. Phần việc phụ trách

Phụ trách xây dựng và bổ sung bộ dữ liệu đánh giá hành vi gọi công cụ của research agent, đồng thời tham gia viết các unit test cho công cụ mới của nhóm. Các đầu việc chính gồm:

* Xây dựng các tình huống đánh giá trong `data/eval\_group.json`, kiểm tra khả năng chọn công cụ, truyền tham số và xử lý ranh giới an toàn.
* Thiết kế tình huống single-turn và multi-turn để đánh giá khả năng xử lý yêu cầu trực tiếp và thông tin bổ sung qua nhiều lượt hội thoại.
* Viết và rà soát unit test cho tool `deduplicate` trong `tests/test\_tools\_todo.py`.
* Chuẩn bị cách chạy bộ đánh giá và kiểm thử, ghi nhận kết quả để hỗ trợ nhóm điều chỉnh prompt và khai báo tool.

## 3\. Đóng góp cụ thể

### 3.1. Xây dựng bộ đánh giá nhóm

Chuẩn bị phiên bản `eval\_group\_completed.json` gồm **10 tình huống đánh giá**, trong đó có **5 single-turn** và **5 multi-turn**, theo cấu trúc dataset của bài lab. Các trường hợp bao phủ:

* `timeline`: chọn đúng công cụ và xử lý tên tài khoản.
* `social\_search`: lựa chọn chế độ tìm kiếm bài đăng.
* `lookup`: xác định trường hợp tìm kiếm tin tức và tham số liên quan.
* `fetch`: lấy nội dung từ URL cụ thể.
* `send`: kiểm tra yêu cầu xác nhận trước khi gửi.
* Multi-turn: sử dụng thông tin người dùng bổ sung ở lượt sau, tránh đoán tham số hoặc thực hiện hành động khi chưa đủ điều kiện.

Các case được gắn `id`, `phase`, `failure\_type`, `expect` và thông tin mô tả mục tiêu kiểm thử theo yêu cầu của README. Bộ case này cần được đồng bộ với `tools.yaml` và code chạy eval của repository trước khi sử dụng chính thức. **Chưa có case riêng cho `deduplicate` trong bản 10 case đã chuẩn bị**; đây là phần cần bổ sung để đáp ứng đầy đủ yêu cầu đánh giá tool mới.

### 3.2. Unit test cho công cụ `deduplicate`

Trong file `test\_tools\_todo.py` đã có **6 hàm test** dành cho `deduplicate`, bao gồm:

1. `test\_deduplicate\_preserves\_optional\_metadata`: kiểm tra giữ lại metadata tùy chọn.
2. `test\_deduplicate\_rejects\_non\_string\_url`: kiểm tra URL không phải chuỗi.
3. `test\_deduplicate\_invalid\_later\_item\_returns\_error\_without\_partial\_output`: kiểm tra dữ liệu lỗi ở phần tử sau không trả về kết quả dở dang.
4. `test\_deduplicate\_keeps\_first\_item\_and\_original\_order`: kiểm tra giữ phần tử xuất hiện đầu tiên và thứ tự gốc khi loại trùng.
5. `test\_deduplicate\_accepts\_empty\_list`: kiểm tra trường hợp danh sách rỗng.
6. `test\_deduplicate\_invalid\_input\_returns\_error`: kiểm tra đầu vào không hợp lệ.

Các test bao phủ đường chạy bình thường và nhiều trường hợp dữ liệu biên. Đây là **các test đã có trong file được cung cấp**, chưa có kết quả chạy thực tế để khẳng định tất cả đều PASS.

### 3.3. Quy trình kiểm tra và tích hợp

Các lệnh dự kiến chạy từ thư mục `starter\_v0`:

```bash
# Chạy riêng các test của deduplicate
pytest -v tests/test\_tools\_todo.py -k deduplicate

# Chạy toàn bộ unit test
pytest -v

# Chạy bộ eval nhóm sau khi đồng bộ tools và prompt
python run\_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval\_group.json
```

Sau khi chạy, cần đối chiếu số case PASS/FAIL, lỗi routing, lỗi arguments và kết quả kiểm thử; chỉ ghi các metric thực tế vào báo cáo nhóm.

## 4\. Bằng chứng

* **File đã chuẩn bị / rà soát:** `data/eval\_group.json` (bản nội dung chuẩn bị: `eval\_group\_completed.json`), `tests/test\_tools\_todo.py`.
* **AI/công cụ đã dùng:** ChatGPT hỗ trợ phân tích yêu cầu trong README, soạn và rà soát các trường hợp eval, giải thích cấu trúc unit test; Git/GitHub dùng để quản lý phiên bản; pytest dùng để kiểm tra code; `run\_eval.py` dùng để đánh giá hành vi gọi tool của agent.

## 5\. Tự đánh giá

Qua phần việc này, mình hiểu rõ hơn sự khác biệt giữa **agent eval** và **unit test**: agent eval kiểm tra mô hình có lựa chọn đúng công cụ và tham số hay không, trong khi unit test kiểm tra bản thân công cụ xử lý đầu vào và lỗi có đúng hay không. Rèn luyện cách xây dựng các trường hợp biên, tình huống nhiều lượt và kiểm tra điều kiện xác nhận trước khi thực hiện hành động.



