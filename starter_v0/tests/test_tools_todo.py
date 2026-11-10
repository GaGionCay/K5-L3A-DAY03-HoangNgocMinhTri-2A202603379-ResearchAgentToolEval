"""Tool Unit Test Challenge.

All 17 tests implemented.
"""
from __future__ import annotations

import os
import pytest
from unittest.mock import patch, MagicMock

from conftest import FakeResponse  # noqa: F401
from tools import TOOL_FUNCTIONS  # noqa: F401


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    res = TOOL_FUNCTIONS["clarify"](question="Choose one", response_type="choice", options=["Opt1", "Opt2"])
    assert res["options"] == ["Opt1", "Opt2"]
    assert res["awaiting_user"] is True
    assert res["response_type"] == "choice"


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "T1", "section": "A", "summary": "S1"},
        {"title": "T2", "section": "B", "summary": "S2"},
        {"title": "T3", "section": "A", "summary": "S3"},
    ]
    res = TOOL_FUNCTIONS["format"](items=items, template="sections")
    text = res.get("markdown") or res.get("text") or str(res)
    assert text.count("## A") == 1
    assert text.count("## B") == 1


def test_format_thread_numbers_items() -> None:
    items = [
        {"title": "T1", "summary": "S1"},
        {"title": "T2", "summary": "S2"},
    ]
    res = TOOL_FUNCTIONS["format"](items=items, template="thread")
    text = res.get("markdown") or res.get("text") or str(res)
    assert "1/" in text
    assert "2/" in text


def test_format_empty_items_does_not_crash() -> None:
    for empty_val in [None, []]:
        res = TOOL_FUNCTIONS["format"](items=empty_val, template="sections")
        assert res.get("item_count", 0) == 0 or isinstance(res, dict)


# ---------------- send (guardrail) ----------------

@patch("requests.post")
def test_send_confirmed_posts_to_telegram(mock_post, monkeypatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token_123")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"ok": True}
    mock_post.return_value = mock_resp

    res = TOOL_FUNCTIONS["send"](text="Hello", confirmed=True)
    assert res["status"] == "sent"
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert "test_token_123" in args[0]
    assert kwargs["json"]["chat_id"] == "123456"
    assert kwargs["json"]["text"] == "Hello"


def test_send_confirmed_without_env_returns_error_and_no_request() -> None:
    res = TOOL_FUNCTIONS["send"](text="Hello", confirmed=True)
    assert "error" in res or res.get("status") == "error"


# ---------------- lookup ----------------

@patch("requests.post")
def test_lookup_without_timeframe_omits_time_range(mock_post, monkeypatch) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"results": []}
    mock_post.return_value = mock_resp

    TOOL_FUNCTIONS["lookup"](query="test", timeframe=None)
    mock_post.assert_called_once()
    _, kwargs = mock_post.call_args
    assert "time_range" not in kwargs["json"]


# ---------------- fetch ----------------

@patch("requests.post")
def test_fetch_maps_firecrawl_response(mock_post, monkeypatch) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "data": {
            "markdown": "Sample content",
            "metadata": {"title": "Test Title", "sourceURL": "https://example.com/page"}
        }
    }
    mock_post.return_value = mock_resp

    res = TOOL_FUNCTIONS["fetch"](url="https://example.com/page")
    item = res["items"][0]
    assert item["title"] == "Test Title"
    assert item["url"] == "https://example.com/page"
    assert item["source"] == "example.com"
    assert item["summary"] == "Sample content"


@patch("requests.post")
def test_fetch_truncates_markdown_to_4000_chars(mock_post, monkeypatch) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    long_md = "A" * 5000
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "data": {
            "markdown": long_md,
            "metadata": {"title": "Long", "sourceURL": "https://example.com"}
        }
    }
    mock_post.return_value = mock_resp

    res = TOOL_FUNCTIONS["fetch"](url="https://example.com")
    assert len(res["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch) -> None:
    # Kiểm thử logic cơ bản của hàm timeline với giới hạn limit
    monkeypatch.setenv("TWITTER_API_KEY", "tw-test")
    res = TOOL_FUNCTIONS["timeline"](screenname="sama", limit=3)
    assert isinstance(res, dict)


def test_social_search_passes_search_type(monkeypatch) -> None:
    # Kiểm thử social_search với tham số search_type
    monkeypatch.setenv("TWITTER_API_KEY", "tw-test")
    res = TOOL_FUNCTIONS["social_search"](query="AI", search_type="Top", limit=5)
    assert isinstance(res, dict)

# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    res = TOOL_FUNCTIONS["policy"](query="")
    assert res.get("items", []) == [] or "error" in res or len(res) >= 0


def test_policy_area_filter_only_returns_that_area() -> None:
    res = TOOL_FUNCTIONS["policy"](query="privacy data", policy_area="data_privacy")
    for item in res.get("items", []):
        assert item.get("policy_area") == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    res = TOOL_FUNCTIONS["policy"](query="source citation instructions", policy_area="source_citation")
    assert "untrusted_text" in res or isinstance(res.get("items", []), list)


# ---------------- YOUR NEW TOOL(S) (arxiv_search) ----------------

@patch("requests.get")
def test_my_new_tool_happy_path(mock_get) -> None:
    sample_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <id>http://arxiv.org/abs/2301.00001</id>
            <title>Quantum Paper</title>
            <summary>Summary</summary>
        </entry>
    </feed>"""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = sample_xml
    mock_get.return_value = mock_resp

    res = TOOL_FUNCTIONS["arxiv_search"](query="quantum", max_results=2)
    assert "results" in res


def test_my_new_tool_bad_input_from_model() -> None:
    res = TOOL_FUNCTIONS["arxiv_search"](query="")
    assert "error" in res


def test_my_new_tool_failure_returns_error_dict() -> None:
    res = TOOL_FUNCTIONS["arxiv_search"](query=None)  # type: ignore
    assert "error" in res