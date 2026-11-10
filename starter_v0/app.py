import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import streamlit as st

import chat as chat_runtime
from chat import now_iso, run_model_tool_loop, write_transcript
from providers import make_provider
try:
    from time_context import current_time_context
except ModuleNotFoundError as exc:
    if exc.name != "time_context":
        raise

    def current_time_context():
        local = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7)))
        return {
            "current_datetime": local.isoformat(timespec="seconds"),
            "current_date": local.date().isoformat(),
            "display_date": local.strftime("%d/%m/%Y"),
            "timezone": "Asia/Ho_Chi_Minh",
            "utc_offset": "+07:00",
        }

from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).resolve().parent
PROMPT_PATH = ROOT / "artifacts" / "system_prompt.md"
TOOLS_PATH = ROOT / "artifacts" / "tools.yaml"
APP_VERSION = "v6-date-context"
CHAT_HAS_TIME_CONTEXT = callable(getattr(chat_runtime, "time_context_message", None))

st.set_page_config(
    page_title="Research Agent",
    page_icon="🔎",
    layout="centered",
)


def new_session():
    version = build_artifact_version(APP_VERSION, PROMPT_PATH, TOOLS_PATH)
    session_id = f"ui_{APP_VERSION}_{uuid4().hex}"
    return {
        "history": [],
        "prompt": PROMPT_PATH.read_text(encoding="utf-8"),
        "tools": to_openai_tools(load_tool_declarations(TOOLS_PATH)),
        "path": ROOT / "transcripts" / f"{session_id}.transcript.json",
        "transcript": {
            "transcript_id": session_id,
            **artifact_version_dict(version),
            "provider": "openrouter",
            "interface": "streamlit",
            "date_context_source": "shared-chat" if CHAT_HAS_TIME_CONTEXT else "ui-fallback",
            "created_at": now_iso(),
            "turns": [],
        },
    }


if "research_session" not in st.session_state:
    st.session_state.research_session = new_session()

with st.sidebar:
    st.header("Research Agent")
    st.write("Tìm tin web, theo dõi X/Twitter và đọc bài viết.")
    if st.button("Cuộc trò chuyện mới"):
        st.session_state.research_session = new_session()
        st.rerun()

session = st.session_state.research_session

st.title("🔎 Research Agent")
st.caption("Bạn muốn tìm hiểu thông tin gì hôm nay?")
st.caption(f"Hôm nay: {current_time_context()['display_date']} · Giờ Việt Nam (UTC+7)")

for message in session["history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Nhập câu hỏi hoặc dán URL bài viết...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    turn = {
        "turn_index": len(session["transcript"]["turns"]) + 1,
        "started_at": now_iso(),
        "user": query,
    }

    runtime_context = current_time_context()
    turn["runtime_context"] = runtime_context
    messages = [
        {"role": "system", "content": session["prompt"]},
        *session["history"][-12:],
        {"role": "user", "content": query},
    ]
    # The integrated chat loop injects its own clock. Supply one only for starter.
    if not CHAT_HAS_TIME_CONTEXT:
        messages.insert(1, {
            "role": "system",
            "content": (
                "Current local date from the application clock: "
                + runtime_context["current_date"]
                + ". Current local time: " + runtime_context["current_datetime"]
                + ". User timezone: Asia/Ho_Chi_Minh (UTC+07:00). "
                + "Resolve today and hôm nay against this clock."
            ),
        })

    try:
        with st.spinner("Đang tìm và tổng hợp thông tin..."):
            provider = make_provider("openrouter")
            result = run_model_tool_loop(
                provider=provider,
                messages=messages,
                tools=session["tools"],
                model=None,
                max_tool_rounds=4,
            )

        turn.update(result)
        session["transcript"]["model"] = getattr(
            provider, "default_model", None
        )

        if result["status"] == "max_tool_rounds":
            answer = (
                "Mình chưa hoàn tất yêu cầu trong lượt này. "
                "Bạn thử thu hẹp chủ đề hoặc số kết quả nhé."
            )
        else:
            answer = result["assistant_text"] or (
                "Chưa có câu trả lời. Bạn thử diễn đạt lại yêu cầu nhé."
            )

        session["history"].extend([
            {"role": "user", "content": query},
            {"role": "assistant", "content": answer},
        ])

    except Exception as exc:
        turn.update({
            "status": "provider_error",
            "error": type(exc).__name__,
        })
        st.error(
            "Chưa xử lý được yêu cầu. "
            "Hãy kiểm tra kết nối và cấu hình provider."
        )

    turn["ended_at"] = now_iso()
    session["transcript"]["turns"].append(turn)
    write_transcript(session["path"], session["transcript"])

    if turn["status"] != "provider_error":
        st.rerun()

if session["transcript"]["turns"]:
    st.sidebar.download_button(
        "Tải transcript",
        data=json.dumps(
            session["transcript"],
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        file_name=session["path"].name,
        mime="application/json",
    )
