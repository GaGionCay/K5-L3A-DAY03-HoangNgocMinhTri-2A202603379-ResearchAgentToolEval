# Đối chiếu repo nộp bài và bản Cloud — 10/11/2026

Đối chiếu theo yêu cầu từ REPORT B4.1. Đây là kết quả kiểm tra tại thời điểm lập tài liệu, không đảm bảo hai remote sẽ luôn đồng bộ sau các lần push tiếp theo.

## Remote và commit

Lệnh chỉ đọc `git ls-remote <remote> refs/heads/ntc` trả cùng commit:

| Remote | Repository | Branch | Commit |
|---|---|---|---|
| origin | GaGionCay/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval | ntc | 9b3cc2940eb20c0895da5dbebe5cbb09bbe76804 |
| streamlit | chill2004/K5-L3A-DAY03-HoangNgocMinhTri-2A202603379-ResearchAgentToolEval | ntc | 9b3cc2940eb20c0895da5dbebe5cbb09bbe76804 |

## Vì sao artifact hash khác nhau?

`versioning.py:file_hash` tính SHA256 trên bytes nguyên bản. File trên Windows chứa CRLF; phiên bản LF cho đúng hash trong transcript Cloud. Chỉ thay CRLF thành LF trong bộ nhớ đã thu được cả hai hash Cloud, không thay nội dung prompt/tools.

| File | SHA256 local CRLF | SHA256 sau chuẩn hóa LF | SHA256 transcript Cloud |
|---|---|---|---|
| `artifacts/system_prompt.md` | `cf82e7a93a6b0fa879bfd7e7da7b2dba8cc5faee6786d6425058c3b4747aa186` | `c5fd2628fcf26cc0765af32ff5f75c1336d4aaa83d84733ab3cd9473c0e56feb` | `c5fd2628fcf26cc0765af32ff5f75c1336d4aaa83d84733ab3cd9473c0e56feb` |
| `artifacts/tools.yaml` | `0bedf4dee6f6bb441ca2aa643bbcbd8c9836f0a50557efbb2ed48c3f8c8e831d` | `190818f266ea69b63d552b9f0a939295d7a8a7d70771f328105b3ef5b1ae6da1` | `190818f266ea69b63d552b9f0a939295d7a8a7d70771f328105b3ef5b1ae6da1` |

Transcript: [ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json](../transcripts/ui_v6-date-context_48233e87253141f3b1511624408b2be5.transcript.json). Artifact local/eval `v6-date-context+pcf82e7a93a6b+t0bedf4dee6f6`; Cloud `v6-date-context+pc5fd2628fcf2+t190818f266ea`.

**Kết luận:** prompt/tools khớp nội dung sau chuẩn hóa xuống dòng. Nhận xét trước về khả năng khác nội dung đã được đính chính; không cần đổi prompt/tools chỉ để ép hash trùng. Giữ nguyên run, transcript và hash lịch sử. Chưa đổi thuật toán versioning trong lần đối chiếu này.

## Những gì kết quả này chưa chứng minh

- Không có commit ID trong transcript nên không khẳng định commit đang chạy trong process Cloud chỉ từ nhãn version. Hai remote cùng commit và hash nội dung khớp là bằng chứng hiện có.
- Eval chạy `ResearchAgent.run`; UI/CLI chạy vòng `run_model_tool_loop` có runtime date context. Điểm base 18/20 và group 10/10 thuộc hai run đã lưu, không phải điểm chấm phiên live hay giá thị trường.
- Transcript cho thấy ngày UTC+7 đúng; độ mới và đơn vị của giá chưa xác minh đầy đủ. Lỗi suy diễn topic thành handle trong phiên CLI cũ vẫn cần regression riêng.
- Không gọi lại API có phí, không sửa code/README, không commit/push trong bước đối chiếu.

Việc tiếp theo và người phụ trách: [TASK_ALLOCATION.md](TASK_ALLOCATION.md).
