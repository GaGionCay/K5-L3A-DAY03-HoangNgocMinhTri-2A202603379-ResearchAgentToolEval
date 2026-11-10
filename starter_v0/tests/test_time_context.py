"""Date grounding and source freshness use the Vietnam clock, not model memory."""
import copy
from datetime import datetime, timezone

import pytest

import chat
from conftest import FakeResponse
from providers.base import ModelResponse, ToolCall
from time_context import current_time_context, time_context_message
from tools import TOOL_FUNCTIONS


@pytest.mark.parametrize("utc_time,expected", [
    ("2026-11-09T18:00:00+00:00", "2026-11-10"),
    ("2026-11-10T00:00:00+00:00", "2026-11-10"),
    ("2026-11-10T16:59:59+00:00", "2026-11-10"),
    ("2026-11-10T17:00:00+00:00", "2026-11-11"),
    ("2026-12-31T18:00:00+00:00", "2027-01-01"),
])
def test_vietnam_date_is_correct_across_utc_midnight_and_year_boundary(utc_time, expected):
    context = current_time_context(datetime.fromisoformat(utc_time))
    assert context["current_date"] == expected
    assert context["current_datetime"].endswith("+07:00")
    assert context["timezone"] == "Asia/Ho_Chi_Minh"


def test_naive_time_is_rejected_instead_of_assuming_cloud_timezone():
    with pytest.raises(ValueError, match="timezone"):
        current_time_context(datetime(2026, 11, 10))


def test_runtime_message_distinguishes_today_from_source_and_retrieval_dates():
    context = current_time_context(datetime(2026, 11, 10, tzinfo=timezone.utc))
    message = time_context_message(context)
    assert message["role"] == "system"
    assert "2026-11-10 (10/11/2026)" in message["content"]
    assert "published_date" in message["content"]
    assert "retrieved_at" in message["content"]
    assert "Never relabel an older quote" in message["content"]


class RecordingProvider:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []

    def complete(self, messages, tools=None, **kwargs):
        self.messages.append(copy.deepcopy(messages))
        return next(self.responses)


def run_loop(provider, messages=None, rounds=4):
    return chat.run_model_tool_loop(
        provider=provider,
        messages=messages or [{"role": "user", "content": "Giá hôm nay?"}],
        tools=[], model=None, max_tool_rounds=rounds,
    )


def test_loop_injects_current_date_and_keeps_caller_history_unchanged(monkeypatch):
    context = current_time_context(datetime(2026, 11, 10, tzinfo=timezone.utc))
    monkeypatch.setattr(chat, "current_time_context", lambda: context)
    history = [
        {"role": "system", "content": "Research assistant"},
        {"role": "assistant", "content": "Older result dated 07/11/2026"},
        {"role": "user", "content": "Giá hôm nay?"},
    ]
    before = copy.deepcopy(history)
    provider = RecordingProvider([ModelResponse(text="Answer", tool_calls=[])])
    result = run_loop(provider, history)
    assert history == before
    assert provider.messages[0][0] == history[0]
    assert provider.messages[0][1]["role"] == "system"
    assert "2026-11-10" in provider.messages[0][1]["content"]
    assert result["runtime_context"] == context


def test_context_refreshes_for_each_turn_in_a_session_open_over_midnight(monkeypatch):
    contexts = iter([
        current_time_context(datetime(2026, 11, 10, 16, 59, tzinfo=timezone.utc)),
        current_time_context(datetime(2026, 11, 10, 17, 1, tzinfo=timezone.utc)),
    ])
    monkeypatch.setattr(chat, "current_time_context", lambda: next(contexts))
    provider = RecordingProvider([ModelResponse(text="A", tool_calls=[]), ModelResponse(text="B", tool_calls=[])])
    assert run_loop(provider)["runtime_context"]["current_date"] == "2026-11-10"
    assert run_loop(provider)["runtime_context"]["current_date"] == "2026-11-11"


@pytest.mark.parametrize("calls,expected", [
    ([], "answered"),
    ([ToolCall("clarify", {"question": "Bạn cần loại giá nào?"})], "waiting_for_user"),
    ([ToolCall("format", {"items": [], "template": "bullets"})], "max_tool_rounds"),
])
def test_all_loop_exit_states_record_the_clock_used(calls, expected):
    result = run_loop(RecordingProvider([ModelResponse(text="Response", tool_calls=calls)]), rounds=1)
    assert result["status"] == expected
    assert result["runtime_context"]["utc_offset"] == "+07:00"


def test_lookup_omits_date_window_unless_explicitly_requested(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"]("giá vàng SJC")
    assert "time_range" not in calls[0]["json"]
    assert "max_age_hours" not in calls[0]["json"]
    assert calls[0]["json"]["include_published_date"] is True
    assert result["timeframe"] is None


@pytest.mark.parametrize("hours", [0, 1, "0", 720])
def test_lookup_sends_explicit_cache_freshness_for_live_pages(hours, monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"]("giá vàng SJC", max_age_hours=hours)
    assert calls[0]["json"]["max_age_hours"] == int(hours)
    assert "time_range" not in calls[0]["json"]
    assert result["max_age_hours"] == int(hours)


@pytest.mark.parametrize("hours", [-1, True, 721, "bad", 1.5])
def test_lookup_invalid_cache_freshness_returns_error_without_http(hours, fake_http):
    calls = fake_http(FakeResponse({}))
    assert TOOL_FUNCTIONS["lookup"]("price", max_age_hours=hours)["error"] == "ValueError"
    assert calls == []


def test_lookup_preserves_source_date_without_replacing_it_by_today(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    date = "Sat, 07 Nov 2026 08:00:00 GMT"
    fake_http(FakeResponse({"results": [{"url": "https://example.com/quote", "published_date": date}]}))
    result = TOOL_FUNCTIONS["lookup"]("price", max_age_hours=0)
    assert result["items"][0]["published_date"] == date
    assert result["retrieved_at"].endswith("+07:00")


def test_lookup_does_not_invent_missing_source_timestamp(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    fake_http(FakeResponse({"results": [{"url": "https://example.com/quote"}]}))
    result = TOOL_FUNCTIONS["lookup"]("price")
    assert "published_date" not in result["items"][0]


def test_news_day_filter_remains_available(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({"results": []}))
    TOOL_FUNCTIONS["lookup"]("robotics", topic="news", timeframe="day")
    assert calls[0]["json"]["topic"] == "news"
    assert calls[0]["json"]["time_range"] == "day"


def test_tool_round_keeps_source_date_and_today_context_separate(monkeypatch, fake_http):
    context = current_time_context(datetime(2026, 11, 10, tzinfo=timezone.utc))
    monkeypatch.setattr(chat, "current_time_context", lambda: context)
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    source_date = "Sat, 07 Nov 2026 08:00:00 GMT"
    fake_http(FakeResponse({"results": [{"url": "https://example.com/price", "published_date": source_date}]}))
    provider = RecordingProvider([
        ModelResponse(text=None, tool_calls=[ToolCall("lookup", {"query": "giá vàng 10/11/2026", "max_age_hours": 0})]),
        ModelResponse(text="Test response only", tool_calls=[]),
    ])
    result = run_loop(provider)
    system_messages = [message["content"] for message in provider.messages[1] if message["role"] == "system"]
    assert any("2026-11-10" in message for message in system_messages)
    assert source_date in provider.messages[1][-1]["content"]
    assert result["tool_events"][0]["result"]["items"][0]["published_date"] == source_date
