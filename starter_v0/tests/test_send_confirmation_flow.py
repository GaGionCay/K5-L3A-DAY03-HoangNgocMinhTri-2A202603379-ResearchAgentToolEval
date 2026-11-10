from __future__ import annotations

from typing import Any

import pytest

import chat
from conftest import FakeResponse
from providers.base import ModelResponse, ToolCall
from tools.send.tool import _approve_send_after_user_confirmation


class SingleResponseProvider:
    def __init__(self, response: ModelResponse) -> None:
        self.response = response
        self.calls = 0

    def complete(self, messages, tools=None, *, model=None, temperature=0.0, tool_choice=None):
        self.calls += 1
        return self.response


def test_send_call_is_intercepted_and_shows_exact_draft_before_confirmation(
    monkeypatch: pytest.MonkeyPatch,
    fake_http,
) -> None:
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "@research_channel")
    http_calls = fake_http(FakeResponse({"ok": True}))
    provider = SingleResponseProvider(ModelResponse(tool_calls=[
        ToolCall("send", {
            "text": "Approved copy",
            "confirmed": True,
            "approval": {"text": "Approved copy", "destination": "@research_channel"},
        }),
        ToolCall("send", {"text": "second action", "confirmed": True}),
    ]))

    result = chat.run_model_tool_loop(
        provider=provider,
        messages=[{"role": "user", "content": "Send the message"}],
        tools=[],
        model=None,
        max_tool_rounds=3,
    )

    assert result["status"] == "waiting_for_user"
    assert result["pending_send"] == {
        "text": "Approved copy",
        "destination": "@research_channel",
    }
    assert "Approved copy" in result["assistant_text"]
    assert "@research_channel" in result["assistant_text"]
    assert result["tool_events"][0]["result"]["status"] == "needs_confirmation"
    assert result["tool_events"][1]["tool"] == "clarify"
    assert result["tool_events"][1]["args"]["response_type"] == "yes_no"
    assert provider.calls == 1
    assert http_calls == []


def test_clarify_confirmation_binds_the_displayed_draft_and_destination(
    monkeypatch: pytest.MonkeyPatch,
    fake_http,
) -> None:
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "@research_channel")
    http_calls = fake_http(FakeResponse({"ok": True}))
    provider = SingleResponseProvider(ModelResponse(tool_calls=[
        ToolCall("clarify", {
            "question": "Send now?",
            "response_type": "yes_no",
            "draft": "Exact message",
            "destination": "@research_channel",
        }),
    ]))

    result = chat.run_model_tool_loop(
        provider=provider,
        messages=[{"role": "user", "content": "Prepare a Telegram post"}],
        tools=[],
        model=None,
        max_tool_rounds=3,
    )

    assert result["status"] == "waiting_for_user"
    assert result["pending_send"] == {
        "text": "Exact message",
        "destination": "@research_channel",
    }
    assert "Exact message" in result["assistant_text"]
    assert "@research_channel" in result["assistant_text"]
    assert result["tool_events"][0]["args"]["response_type"] == "yes_no"
    assert http_calls == []


def test_clarify_with_missing_destination_requests_text_not_approval(
    monkeypatch: pytest.MonkeyPatch,
    fake_http,
) -> None:
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    http_calls = fake_http(FakeResponse({"ok": True}))
    provider = SingleResponseProvider(ModelResponse(tool_calls=[
        ToolCall("clarify", {
            "question": "Send now?",
            "response_type": "yes_no",
            "draft": "Exact message",
        }),
    ]))

    result = chat.run_model_tool_loop(
        provider=provider,
        messages=[{"role": "user", "content": "Prepare a Telegram post"}],
        tools=[],
        model=None,
        max_tool_rounds=3,
    )

    assert result["status"] == "waiting_for_user"
    assert "Which Telegram chat ID or channel" in result["assistant_text"]
    assert "pending_send" not in result
    assert result["tool_events"][0]["args"]["response_type"] == "text"
    assert http_calls == []


def test_yes_after_displayed_draft_sends_only_that_draft_and_destination(
    monkeypatch: pytest.MonkeyPatch,
    fake_http,
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "@configured_channel")
    http_calls = fake_http(FakeResponse({"ok": True}))
    pending = {"text": "The exact draft", "destination": "@approved_channel"}

    result = chat.resolve_pending_send("yes", pending)

    assert result["status"] == "send_sent"
    assert len(http_calls) == 1
    assert http_calls[0]["json"] == {
        "chat_id": "@approved_channel",
        "text": "The exact draft",
        "parse_mode": "Markdown",
    }
    assert result["tool_events"][0]["args"]["confirmed"] is True


@pytest.mark.parametrize("reply", ["please send it", "yes, but change the text"])
def test_ambiguous_reply_does_not_send_and_keeps_confirmation_pending(
    reply: str,
    monkeypatch: pytest.MonkeyPatch,
    fake_http,
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    http_calls = fake_http(FakeResponse({"ok": True}))

    result = chat.resolve_pending_send(
        reply,
        {"text": "The exact draft", "destination": "@approved_channel"},
    )

    assert result["status"] == "waiting_for_user"
    assert http_calls == []


def test_explicit_no_cancels_without_sending(fake_http) -> None:
    http_calls = fake_http(FakeResponse({"ok": True}))

    result = chat.resolve_pending_send(
        "no",
        {"text": "The exact draft", "destination": "@approved_channel"},
    )

    assert result["status"] == "send_cancelled"
    assert http_calls == []


def test_approval_is_bound_to_exact_draft_and_destination(monkeypatch: pytest.MonkeyPatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    http_calls = fake_http(FakeResponse({"ok": True}))
    approval = _approve_send_after_user_confirmation("Original draft", "@approved_channel")

    result = chat.TOOL_FUNCTIONS["send"](
        text="Changed draft",
        confirmed=True,
        destination="@approved_channel",
        approval=approval,
    )

    assert result["status"] == "needs_confirmation"
    assert http_calls == []
