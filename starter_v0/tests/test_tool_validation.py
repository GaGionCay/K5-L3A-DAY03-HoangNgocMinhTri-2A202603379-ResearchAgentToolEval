"""Model-input edge cases and failures must return errors without side effects."""
from __future__ import annotations

import importlib
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import pytest
import requests

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS as T


@pytest.mark.parametrize("name,args", [
    ("clarify", {"question": ""}),
    ("clarify", {"question": "Q", "response_type": "invalid"}),
    ("clarify", {"question": "Q", "response_type": "choice", "options": ["one"]}),
    ("clarify", {"question": "Q", "options": "not a list"}),
    ("format", {"items": "bad"}),
    ("format", {"items": [1]}),
    ("format", {"template": "unknown"}),
    ("format", {"items": [{"title": 123}]}),
    ("timeline", {"screenname": ""}),
    ("timeline", {"screenname": "name with spaces"}),
    ("timeline", {"screenname": "nasa", "limit": 0}),
    ("timeline", {"screenname": "nasa", "limit": -1}),
    ("timeline", {"screenname": "nasa", "limit": True}),
    ("social_search", {"query": ""}),
    ("social_search", {"query": "AI", "search_type": "latest"}),
    ("social_search", {"query": "AI", "limit": 0}),
    ("lookup", {"query": ""}),
    ("lookup", {"query": None}),
    ("lookup", {"query": "AI", "topic": "tweets"}),
    ("lookup", {"query": "AI", "timeframe": "yesterday"}),
    ("lookup", {"query": "AI", "max_results": 0}),
    ("lookup", {"query": "AI", "max_results": 21}),
    ("fetch", {"url": "https://"}),
    ("fetch", {"url": "file:///etc/passwd"}),
    ("fetch", {"url": None}),
    ("send", {"text": "", "confirmed": True}),
    ("send", {"text": "x" * 4097, "confirmed": True}),
    ("policy", {"query": 3}),
    ("policy", {"query": "privacy", "top_k": 0}),
    ("policy", {"query": "privacy", "policy_area": "made_up"}),
    ("papers", {"query": ""}),
    ("papers", {"query": "agents", "max_results": 0}),
    ("papers", {"query": "agents", "sort_by": "recent"}),
    ("paper_text", {"arxiv_url": "not-an-id"}),
    ("paper_text", {"arxiv_url": "https://example.com/1706.03762"}),
    ("paper_text", {"arxiv_url": "1706.03762", "max_pages": 0}),
    ("paper_text", {"arxiv_url": "1706.03762", "max_chars": 0}),
])
def test_bad_arguments_return_errors_without_network(name, args, fake_http):
    calls = fake_http(FakeResponse({}))
    result = T[name](**args)
    assert result["error"] == "ValueError"
    assert calls == []


@pytest.mark.parametrize("name,args,key", [
    ("lookup", {"query": "AI"}, "TAVILY_API_KEY"),
    ("fetch", {"url": "https://example.com"}, "FIRECRAWL_API_KEY"),
    ("timeline", {"screenname": "nasa"}, "RAPIDAPI_KEY"),
    ("social_search", {"query": "AI"}, "RAPIDAPI_KEY"),
])
def test_missing_api_key_returns_error_without_network(name, args, key, fake_http):
    calls = fake_http(FakeResponse({}))
    result = T[name](**args)
    assert result["error"] == "RuntimeError"
    assert key in result["message"]
    assert calls == []


@pytest.mark.parametrize("name,args,key", [
    ("lookup", {"query": "AI"}, "TAVILY_API_KEY"),
    ("fetch", {"url": "https://example.com"}, "FIRECRAWL_API_KEY"),
    ("timeline", {"screenname": "nasa"}, "RAPIDAPI_KEY"),
    ("social_search", {"query": "AI"}, "RAPIDAPI_KEY"),
])
@pytest.mark.parametrize("failure,expected", [
    (FakeResponse(status_code=429), "HTTPError"),
    (requests.Timeout("offline timeout"), "Timeout"),
])
def test_api_failure_returns_error_dict(name, args, key, failure, expected, monkeypatch, fake_http):
    monkeypatch.setenv(key, "fake-key")
    calls = fake_http(failure)
    result = T[name](**args)
    assert result["error"] == expected
    assert len(calls) == 1


@pytest.mark.parametrize("confirmed", [False, "false", "true", 1, None, []])
def test_send_requires_literal_true_before_any_network(confirmed, fake_http):
    calls = fake_http(FakeResponse({"ok": True}))
    assert T["send"]("Message", confirmed=confirmed)["status"] == "needs_confirmation"
    assert calls == []


def test_send_checks_telegram_api_result(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    calls = fake_http(FakeResponse({"ok": False, "description": "Bad Request"}))
    assert T["send"]("Message", confirmed=True)["error"] == "RuntimeError"
    assert len(calls) == 1


def test_send_http_error_redacts_token(monkeypatch, fake_http):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "secret-test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123")
    fake_http(requests.HTTPError("403 for https://api.telegram.org/botsecret-test-token/sendMessage"))
    result = T["send"]("Message", confirmed=True)
    assert result["error"] == "HTTPError"
    assert "secret-test-token" not in result["message"]


def test_lookup_accepts_string_count_and_caps_mapped_results(monkeypatch, fake_http):
    monkeypatch.setenv("TAVILY_API_KEY", "fake-key")
    calls = fake_http(FakeResponse({"results": [{"url": f"https://example.com/{i}"} for i in range(3)]}))
    result = T["lookup"]("AI", max_results="2")
    assert calls[0]["json"]["max_results"] == 2
    assert len(result["items"]) == 2


def test_timeline_normalizes_handle_and_fills_url_from_known_account(monkeypatch, fake_http):
    monkeypatch.setenv("RAPIDAPI_KEY", "fake-key")
    calls = fake_http(FakeResponse({"timeline": [{"tweet_id": "123", "text": "Space"}]}))
    result = T["timeline"](" @nasa ", limit="1")
    assert calls[0]["params"] == {"screenname": "nasa"}
    assert result["items"][0]["url"] == "https://x.com/nasa/status/123"
    assert "_tweet_id" not in result["items"][0]


def test_fetch_reports_api_level_failure(monkeypatch, fake_http):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fake-key")
    fake_http(FakeResponse({"success": False}))
    assert T["fetch"]("https://example.com")["error"] == "RuntimeError"


def test_format_missing_source_and_url_still_formats():
    result = T["format"]([{"title": "No link"}], template="bullets")
    assert "No link" in result["markdown"]
    assert "None" not in result["markdown"]


def test_policy_accepts_string_limit_and_returns_static_freshness():
    result = T["policy"]("citation", policy_area="source_citation", top_k="1")
    assert len(result["results"]) == 1
    assert result["freshness"] == "static_company_policy"


ATOM_FEED = '''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:arxiv="http://arxiv.org/schemas/atom">
<opensearch:totalResults>1</opensearch:totalResults><entry>
<id>https://arxiv.org/abs/1706.03762v1</id><title>Attention Is All You Need</title>
<summary>Example abstract.</summary><author><name>Example Author</name></author>
<published>2017-06-12</published><updated>2017-06-12</updated>
<link title="pdf" href="https://arxiv.org/pdf/1706.03762v1.pdf"/>
<arxiv:primary_category term="cs.CL"/><category term="cs.CL"/>
</entry></feed>'''


@pytest.fixture
def papers_module(monkeypatch):
    module = importlib.import_module("tools.papers.tool")
    monkeypatch.setattr(module, "_rate_limit_arxiv", lambda: None)
    return module


def test_papers_maps_atom_and_request_params(papers_module, fake_http):
    calls = fake_http(FakeResponse(text=ATOM_FEED))
    result = T["papers"]("attention models", max_results="1", sort_by="submittedDate")
    assert calls[0]["url"] == "https://export.arxiv.org/api/query"
    assert calls[0]["params"] == {"search_query": "all:attention AND all:models", "max_results": 1, "sortBy": "submittedDate", "sortOrder": "descending"}
    assert "User-Agent" in calls[0]["headers"]
    assert result["total_results"] == 1
    assert result["items"][0]["arxiv_id"] == "1706.03762v1"
    assert result["items"][0]["authors"] == ["Example Author"]


def test_papers_malformed_xml_returns_error(papers_module, fake_http):
    fake_http(FakeResponse(text="not XML"))
    assert T["papers"]("agents")["error"] == "ParseError"


def test_papers_http_error_returns_error(papers_module, fake_http):
    fake_http(FakeResponse(status_code=503))
    assert T["papers"]("agents")["error"] == "HTTPError"


def test_papers_retries_429_then_succeeds(papers_module, monkeypatch):
    replies = iter([FakeResponse(status_code=429), FakeResponse(text=ATOM_FEED)])
    calls = []
    monkeypatch.setattr(papers_module.time, "sleep", lambda _: None)
    def get(url, **kwargs):
        calls.append(url)
        return next(replies)
    monkeypatch.setattr(papers_module.requests, "get", get)
    assert len(T["papers"]("agents")["items"]) == 1
    assert len(calls) == 2


@pytest.fixture
def pdf_module(monkeypatch):
    # A unique directory per test avoids pytest's shared pytest-of-<user>
    # directory, which may be owned by a different Windows execution context.
    with TemporaryDirectory(prefix="day03-pdf-test-") as directory:
        module = importlib.import_module("tools.paper_text.tool")
        monkeypatch.setattr(module, "ARXIV_DIR", Path(directory) / "papers")
        monkeypatch.setattr(module, "_rate_limit_arxiv", lambda: None)
        yield module


def test_paper_text_downloads_and_parses_real_pdf_offline(pdf_module, fake_http):
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buffer = BytesIO()
    writer.write(buffer)
    response = FakeResponse(content=buffer.getvalue())
    response.iter_content = lambda chunk_size: iter([response.content])
    calls = fake_http(response)
    result = T["paper_text"]("https://arxiv.org/abs/1706.03762v1", max_pages=1)
    assert calls[0]["url"] == "https://arxiv.org/pdf/1706.03762v1.pdf"
    assert calls[0]["stream"] is True
    assert result["page_count"] == 1
    assert result["pages_read"] == 1
    assert result["chars_returned"] == 0
    assert (pdf_module.ARXIV_DIR / "1706.03762v1.pdf").read_bytes() == response.content
    assert (pdf_module.ARXIV_DIR / "1706.03762v1.txt").read_text() == ""


def test_paper_text_honors_page_and_character_limits(pdf_module, monkeypatch, fake_http):
    import pypdf
    response = FakeResponse(content=b"mock-pdf")
    response.iter_content = lambda chunk_size: iter([response.content])
    fake_http(response)
    extracted = []
    def extract(index):
        extracted.append(index)
        return "abcdefghij"
    pages = [SimpleNamespace(extract_text=lambda i=i: extract(i)) for i in range(3)]
    monkeypatch.setattr(pypdf, "PdfReader", lambda _: SimpleNamespace(pages=pages))
    result = T["paper_text"]("1706.03762", max_pages="1", max_chars="4")
    assert extracted == [0]
    assert result["items"][0]["summary"] == "abcd"
    assert result["chars_returned"] == 4
    assert (pdf_module.ARXIV_DIR / "1706.03762.txt").read_text() == "abcd"


def test_paper_text_http_failure_returns_error_without_pdf(pdf_module, fake_http):
    fake_http(FakeResponse(status_code=404))
    result = T["paper_text"]("1706.03762")
    assert result["error"] == "HTTPError"
    assert not list(pdf_module.ARXIV_DIR.glob("*.pdf"))


def test_paper_text_invalid_pdf_returns_error(pdf_module, fake_http):
    response = FakeResponse(content=b"this is not a PDF")
    response.iter_content = lambda chunk_size: iter([response.content])
    fake_http(response)
    result = T["paper_text"]("1706.03762")
    assert "error" in result
    assert not list(pdf_module.ARXIV_DIR.glob("*.txt"))


def test_paper_text_supports_legacy_arxiv_id(pdf_module):
    assert pdf_module._arxiv_id("https://arxiv.org/pdf/hep-th/9901001v2.pdf") == "hep-th/9901001v2"
