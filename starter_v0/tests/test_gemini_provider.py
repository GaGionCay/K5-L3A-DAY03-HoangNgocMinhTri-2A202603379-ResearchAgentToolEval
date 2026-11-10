from __future__ import annotations

import sys
import types
from typing import Any

import pytest

import providers.gemini_provider as gemini_provider


class FakeResourceExhausted(Exception):
    code = 429
    status = "RESOURCE_EXHAUSTED"

    def __init__(self, message: str = "rate limited", details: Any = None) -> None:
        super().__init__(message)
        self.details = details or []


def install_fake_gemini_sdk(monkeypatch: pytest.MonkeyPatch, generate_content) -> None:
    google_module = types.ModuleType("google")
    genai_module = types.ModuleType("google.genai")
    types_module = types.ModuleType("google.genai.types")

    class FakeTool:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs

    class FakeGenerateContentConfig:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs

    class FakeClient:
        def __init__(self, **kwargs: Any) -> None:
            self.models = types.SimpleNamespace(generate_content=generate_content)

    types_module.Tool = FakeTool
    types_module.GenerateContentConfig = FakeGenerateContentConfig
    genai_module.types = types_module
    genai_module.Client = FakeClient
    google_module.genai = genai_module

    monkeypatch.setitem(sys.modules, "google", google_module)
    monkeypatch.setitem(sys.modules, "google.genai", genai_module)
    monkeypatch.setitem(sys.modules, "google.genai.types", types_module)


def test_complete_retries_transient_429_with_exponential_backoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    sleeps: list[float] = []
    monkeypatch.setattr(gemini_provider.time, "sleep", sleeps.append)
    attempts = 0

    def generate_content(**kwargs: Any) -> Any:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise FakeResourceExhausted()
        return types.SimpleNamespace(candidates=[])

    install_fake_gemini_sdk(monkeypatch, generate_content)
    result = gemini_provider.GeminiProvider().complete([{"role": "user", "content": "test"}])

    assert attempts == 3
    assert sleeps == [1.0, 2.0]
    assert result.tool_calls == []


def test_complete_raises_after_retry_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    sleeps: list[float] = []
    monkeypatch.setattr(gemini_provider.time, "sleep", sleeps.append)
    attempts = 0

    def generate_content(**kwargs: Any) -> Any:
        nonlocal attempts
        attempts += 1
        raise FakeResourceExhausted()

    install_fake_gemini_sdk(monkeypatch, generate_content)
    with pytest.raises(FakeResourceExhausted):
        gemini_provider.GeminiProvider().complete([{"role": "user", "content": "test"}])

    assert attempts == gemini_provider.MAX_RATE_LIMIT_RETRIES + 1
    assert sleeps == [1.0, 2.0, 4.0]


def test_complete_honors_retry_info_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    sleeps: list[float] = []
    monkeypatch.setattr(gemini_provider.time, "sleep", sleeps.append)
    attempts = 0

    def generate_content(**kwargs: Any) -> Any:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise FakeResourceExhausted(
                details=[{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "2.5s"}]
            )
        return types.SimpleNamespace(candidates=[])

    install_fake_gemini_sdk(monkeypatch, generate_content)
    gemini_provider.GeminiProvider().complete([{"role": "user", "content": "test"}])

    assert attempts == 2
    assert sleeps == [2.5]


@pytest.mark.parametrize(
    "error",
    [
        FakeResourceExhausted(
            "per day limit exceeded",
            details=[{"quotaId": "GenerateRequestsPerDayPerProject-FreeTier", "retryDelay": "86400s"}],
        ),
        FakeResourceExhausted(
            details=[{"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "120s"}]
        ),
    ],
)
def test_complete_does_not_retry_quota_delays_beyond_cap(
    monkeypatch: pytest.MonkeyPatch,
    error: FakeResourceExhausted,
) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    sleeps: list[float] = []
    monkeypatch.setattr(gemini_provider.time, "sleep", sleeps.append)
    attempts = 0

    def generate_content(**kwargs: Any) -> Any:
        nonlocal attempts
        attempts += 1
        raise error

    install_fake_gemini_sdk(monkeypatch, generate_content)
    with pytest.raises(FakeResourceExhausted):
        gemini_provider.GeminiProvider().complete([{"role": "user", "content": "test"}])

    assert attempts == 1
    assert sleeps == []


def test_complete_does_not_retry_non_rate_limit_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    attempts = 0

    def generate_content(**kwargs: Any) -> Any:
        nonlocal attempts
        attempts += 1
        raise RuntimeError("model not found")

    install_fake_gemini_sdk(monkeypatch, generate_content)
    with pytest.raises(RuntimeError, match="model not found"):
        gemini_provider.GeminiProvider().complete([{"role": "user", "content": "test"}])

    assert attempts == 1
