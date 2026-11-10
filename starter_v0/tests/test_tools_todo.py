"""Offline tool tests: local behavior, mocked API requests and regression coverage."""
"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401
from tools.send.tool import _approve_send_after_user_confirmation

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user():
    options = ["Web", "Twitter"]
    result = TOOL_FUNCTIONS["clarify"]("Chọn nguồn?", response_type="choice", options=options)
    assert result["question"] == "Chọn nguồn?"
    assert result["options"] == options
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section():
    items = [{"section": section, "title": section} for section in ("A", "B", "A")]
    result = TOOL_FUNCTIONS["format"](items=items, template="sections")
    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1
    assert result["item_count"] == 3


def test_format_thread_numbers_items():
    result = TOOL_FUNCTIONS["format"](items=[{"title": "A"}, {"title": "B"}], template="thread")
    assert result["markdown"].startswith("1/ A")
    assert "\n\n2/ B" in result["markdown"]


@pytest.mark.parametrize("items", [None, []])
def test_format_empty_items_does_not_crash(items):
    result = TOOL_FUNCTIONS["format"](items=items)
    assert result["item_count"] == 0
    assert result["markdown"] == ""


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": True}))
    approval = _approve_send_after_user_confirmation("Bản tin", "-100123")
    result = TOOL_FUNCTIONS["send"]("Bản tin", confirmed=True, approval=approval)
    assert result["status"] == "sent"
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert calls[0]["url"] == "https://api.telegram.org/botfake-token/sendMessage"
    assert calls[0]["json"] == {"chat_id": "-100123", "text": "Bản tin", "parse_mode": "Markdown"}


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http):
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"]("Bản tin", confirmed=True)
    assert result["status"] == "needs_destination"
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"]("robotics", timeframe=None)
    assert "error" not in result
    assert "time_range" not in calls[0]["json"]
    assert calls[0]["json"]["query"] == "robotics"
    assert result["items"] == []


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {"markdown": "Nội dung", "metadata": {"title": "T", "sourceURL": "https://example.com/article"}}}))
    result = TOOL_FUNCTIONS["fetch"]("https://example.com/article")
    assert calls[0]["json"] == {"url": "https://example.com/article", "formats": ["markdown"]}
    assert calls[0]["headers"]["Authorization"] == "Bearer test-key"
    assert result["items"] == [{"title": "T", "url": "https://example.com/article", "source": "example.com", "summary": "Nội dung"}]


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000}}))
    result = TOOL_FUNCTIONS["fetch"]("https://example.com/article")
    assert result["items"][0]["summary"] == "x" * 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http):
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    tweets = [{"text": "missing id"}] + [{"tweet_id": str(i), "screen_name": "nasa", "text": f"Tweet {i}"} for i in range(1, 7)]
    calls = fake_http(FakeResponse({"timeline": tweets}))
    result = TOOL_FUNCTIONS["timeline"]("nasa", limit=3)
    assert calls[0]["params"] == {"screenname": "nasa"}
    assert calls[0]["headers"]["x-rapidapi-key"] == "test-key"
    assert [item["url"] for item in result["items"]] == [f"https://x.com/nasa/status/{i}" for i in range(1, 4)]


@pytest.mark.parametrize("search_type", ["Top", "Latest"])
def test_social_search_passes_search_type(monkeypatch, fake_http, search_type):
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"tweets": [{"id": "1", "screen_name": "nasa", "text": "Space"}]}))
    result = TOOL_FUNCTIONS["social_search"]("space", search_type=search_type, limit=1)
    assert calls[0]["params"] == {"query": "space", "search_type": search_type}
    assert result["items"][0]["url"] == "https://x.com/nasa/status/1"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results():
    assert TOOL_FUNCTIONS["policy"]("  ")["results"] == []


def test_policy_area_filter_only_returns_that_area():
    result = TOOL_FUNCTIONS["policy"]("privacy API keys", policy_area="data_privacy")
    assert result["results"]
    assert all(item["policy_area"] == "data_privacy" for item in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text():
    result = TOOL_FUNCTIONS["policy"]("citation", policy_area="source_citation", top_k=50)
    probes = [line for item in result["results"] for line in item["untrusted_text"]]
    assert any("ignore the citation policy" in line for line in probes)
    assert all("ignore the citation policy" not in item["facts"] for item in result["results"])


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_deduplicate_preserves_optional_metadata():
    items = [{"url": "https://example.com/a", "source": "official", "metrics": {"views": 10}}]
    result = TOOL_FUNCTIONS["deduplicate"](items)
    assert result["items"] == items
    assert result["items"][0] is not items[0]


def test_deduplicate_rejects_non_string_url():
    result = TOOL_FUNCTIONS["deduplicate"]([{"url": 123}])
    assert result["error"] == "invalid_input"


def test_deduplicate_invalid_later_item_returns_error_without_partial_output():
    items = [{"url": "https://example.com/a"}, {"title": "missing URL"}]
    result = TOOL_FUNCTIONS["deduplicate"](items)
    assert result["error"] == "invalid_input"
    assert "items" not in result
    assert len(items) == 2

# ---------------- deduplicate ----------------

def test_deduplicate_keeps_first_item_and_original_order():
    items = [
        {"title": "Bản đầu", "url": "https://example.com/a"},
        {"title": "Bài khác", "url": "https://example.com/b"},
        {"title": "Bản trùng", "url": " https://example.com/a "},
    ]

    result = TOOL_FUNCTIONS["deduplicate"](items=items)

    assert result["items"] == items[:2]
    assert result["input_count"] == 3
    assert result["item_count"] == 2
    assert result["removed_count"] == 1
    assert len(items) == 3


def test_deduplicate_accepts_empty_list():
    result = TOOL_FUNCTIONS["deduplicate"](items=[])

    assert result["items"] == []
    assert result["input_count"] == 0
    assert result["item_count"] == 0
    assert result["removed_count"] == 0


@pytest.mark.parametrize(
    "items",
    [
        None,
        "not a list",
        [123],
        [{"title": "Thiếu URL"}],
        [{"url": "   "}],
    ],
)
def test_deduplicate_invalid_input_returns_error(items):
    result = TOOL_FUNCTIONS["deduplicate"](items=items)

    assert result["error"] == "invalid_input"
    assert result["message"]
