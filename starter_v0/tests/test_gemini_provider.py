from __future__ import annotations

import pytest

from providers import gemini_provider


class GeminiApiError(Exception):
    def __init__(self, code: int) -> None:
        super().__init__(f"Gemini status {code}")
        self.code = code


def test_gemini_503_retries_then_returns_response(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0
    delays: list[int] = []
    monkeypatch.setattr(gemini_provider.time, "sleep", delays.append)

    def generate() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise GeminiApiError(503)
        return "response"

    assert gemini_provider._generate_with_retry(generate) == "response"
    assert calls == 3
    assert delays == [2, 4]


def test_gemini_non_503_error_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0
    monkeypatch.setattr(gemini_provider.time, "sleep", lambda _: pytest.fail("unexpected retry"))

    def generate() -> None:
        nonlocal calls
        calls += 1
        raise GeminiApiError(401)

    with pytest.raises(GeminiApiError):
        gemini_provider._generate_with_retry(generate)
    assert calls == 1


def test_gemini_503_is_raised_after_retry_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0
    monkeypatch.setattr(gemini_provider.time, "sleep", lambda _: None)

    def generate() -> None:
        nonlocal calls
        calls += 1
        raise GeminiApiError(503)

    with pytest.raises(GeminiApiError):
        gemini_provider._generate_with_retry(generate)
    assert calls == gemini_provider._UNAVAILABLE_RETRIES + 1
