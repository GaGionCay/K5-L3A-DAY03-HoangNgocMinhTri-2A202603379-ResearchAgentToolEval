from __future__ import annotations

import json
import logging
import os
import re
import time
from typing import Any

from providers.base import ModelResponse, ToolCall


logger = logging.getLogger(__name__)

MAX_RATE_LIMIT_RETRIES = 3
MAX_RETRY_DELAY_SECONDS = 60.0
BASE_RETRY_DELAY_SECONDS = 1.0


def _is_resource_exhausted(exc: Exception) -> bool:
    code = getattr(exc, "code", None)
    if code == 429 or str(code) == "429":
        return True

    status_code = getattr(exc, "status_code", None)
    if status_code == 429:
        return True

    status = getattr(exc, "status", None)
    return str(status).upper() == "RESOURCE_EXHAUSTED"


def _is_daily_quota_error(exc: Exception) -> bool:
    message = str(exc).lower()
    if "per day limit exceeded" in message or "requests per day" in message:
        return True

    def contains_daily_quota(value: Any) -> bool:
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower() in {"quotaid", "description"} and "perday" in str(item).lower().replace("_", ""):
                    return True
                if contains_daily_quota(item):
                    return True
        elif isinstance(value, (list, tuple)):
            return any(contains_daily_quota(item) for item in value)
        return False

    return contains_daily_quota(getattr(exc, "details", None))


def _parse_delay(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return max(0.0, float(value))
    if not isinstance(value, str):
        return None

    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(ms|s|sec|seconds?|m|min|minutes?|h|hours?)?\s*", value, re.I)
    if not match:
        return None
    amount = float(match.group(1))
    unit = (match.group(2) or "s").lower()
    multiplier = 0.001 if unit == "ms" else 60 if unit.startswith("m") else 3600 if unit.startswith("h") else 1
    return amount * multiplier


def _server_retry_delay(exc: Exception) -> float | None:
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", None)
    if headers:
        delay = _parse_delay(headers.get("Retry-After"))
        if delay is not None:
            return delay

    details = getattr(exc, "details", None)

    def find_retry_delay(value: Any) -> float | None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower().replace("_", "") == "retrydelay":
                    delay = _parse_delay(item)
                    if delay is not None:
                        return delay
                delay = find_retry_delay(item)
                if delay is not None:
                    return delay
        elif isinstance(value, (list, tuple)):
            for item in value:
                delay = find_retry_delay(item)
                if delay is not None:
                    return delay
        else:
            delay_value = getattr(value, "retry_delay", None)
            delay = _parse_delay(delay_value)
            if delay is not None:
                return delay
        return None

    delay = find_retry_delay(details)
    if delay is not None:
        return delay

    match = re.search(r"retry in\s+(\d+(?:\.\d+)?)\s*(ms|s|sec|seconds?|m|min|minutes?|h|hours?)", str(exc), re.I)
    return _parse_delay("".join(match.groups())) if match else None


def _retry_delay_seconds(exc: Exception, retry_index: int) -> float | None:
    if _is_daily_quota_error(exc):
        return None

    delay = _server_retry_delay(exc)
    if delay is None:
        delay = min(BASE_RETRY_DELAY_SECONDS * (2**retry_index), MAX_RETRY_DELAY_SECONDS)
    if delay > MAX_RETRY_DELAY_SECONDS:
        return None
    return delay


def _to_gemini_declarations(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    for item in tools or []:
        function = item.get("function", item)
        declarations.append({
            "name": function["name"],
            "description": function.get("description", ""),
            "parameters": function.get("parameters", {"type": "object", "properties": {}}),
        })
    return declarations


def _to_gemini_contents(messages: list[dict[str, str]]) -> tuple[str | None, list[dict[str, Any]]]:
    system_parts: list[str] = []
    contents: list[dict[str, Any]] = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "system":
            system_parts.append(content)
        elif role == "assistant":
            contents.append({"role": "model", "parts": [{"text": content}]})
        elif role == "user":
            contents.append({"role": "user", "parts": [{"text": content}]})
    return ("\n\n".join(system_parts) if system_parts else None), contents


def _part_text(part: Any) -> str | None:
    if hasattr(part, "text"):
        return getattr(part, "text")
    if isinstance(part, dict):
        return part.get("text")
    return None


def _part_function_call(part: Any) -> Any | None:
    if hasattr(part, "function_call"):
        return getattr(part, "function_call")
    if isinstance(part, dict):
        return part.get("function_call")
    return None


def _function_call_name(call: Any) -> str | None:
    if hasattr(call, "name"):
        return getattr(call, "name")
    if isinstance(call, dict):
        return call.get("name")
    return None


def _function_call_args(call: Any) -> dict[str, Any]:
    if hasattr(call, "args"):
        return dict(getattr(call, "args") or {})
    if isinstance(call, dict):
        return dict(call.get("args") or {})
    return {}


class GeminiProvider:
    """Google Gemini API provider with normalized tool_calls output."""

    def __init__(
        self,
        *,
        api_key_env: str = "GEMINI_API_KEY",
        default_model: str = "gemini-3.5-flash",
    ) -> None:
        self.api_key_env = api_key_env
        self.default_model = default_model

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError("Install live provider dependency first: pip install google-genai") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

        system_instruction, contents = _to_gemini_contents(messages)
        declarations = _to_gemini_declarations(tools)
        config_kwargs: dict[str, Any] = {"temperature": temperature}
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if declarations:
            config_kwargs["tools"] = [types.Tool(function_declarations=declarations)]

        client = genai.Client(api_key=api_key)
        for retry_index in range(MAX_RATE_LIMIT_RETRIES + 1):
            try:
                resp = client.models.generate_content(
                    model=model or self.default_model,
                    contents=contents,
                    config=types.GenerateContentConfig(**config_kwargs),
                )
                break
            except Exception as exc:
                if not _is_resource_exhausted(exc) or retry_index >= MAX_RATE_LIMIT_RETRIES:
                    raise

                delay = _retry_delay_seconds(exc, retry_index)
                if delay is None:
                    raise

                logger.warning(
                    "Gemini rate limit hit; retrying attempt %s/%s in %.2f seconds.",
                    retry_index + 1,
                    MAX_RATE_LIMIT_RETRIES,
                    delay,
                )
                time.sleep(delay)

        text_parts: list[str] = []
        calls: list[ToolCall] = []

        def append_call(function_call: Any) -> None:
            name = _function_call_name(function_call)
            if name:
                calls.append(ToolCall(name=name, args=_function_call_args(function_call)))

        for candidate in getattr(resp, "candidates", []) or []:
            content = getattr(candidate, "content", None)
            for part in getattr(content, "parts", []) or []:
                text = _part_text(part)
                if text:
                    text_parts.append(text)
                function_call = _part_function_call(part)
                if function_call:
                    append_call(function_call)

        # Some SDK versions expose function calls directly on the response.
        for function_call in getattr(resp, "function_calls", []) or []:
            append_call(function_call)

        deduped_calls: list[ToolCall] = []
        seen: set[tuple[str, str]] = set()
        for call in calls:
            key = (call.name, json.dumps(call.args, ensure_ascii=False, sort_keys=True))
            if key not in seen:
                seen.add(key)
                deduped_calls.append(call)

        return ModelResponse(text="\n".join(part for part in text_parts if part) or None, tool_calls=deduped_calls, raw=resp)
