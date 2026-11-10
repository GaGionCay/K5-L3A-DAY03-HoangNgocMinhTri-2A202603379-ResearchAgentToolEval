"""Validate model arguments before any network request or file write."""
from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse


def text(value: Any, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    value = value.strip()
    if not value and not allow_empty:
        raise ValueError(f"{name} must not be empty")
    return value


def integer(value: Any, name: str, *, maximum: int | None = None, minimum: int = 1) -> int:
    if isinstance(value, str) and re.fullmatch(r"[0-9]+", value.strip()):
        value = int(value.strip())
    if type(value) is not int or value < minimum:
        description = "non-negative" if minimum == 0 else "positive"
        raise ValueError(f"{name} must be a {description} integer")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be at most {maximum}")
    return value


def choice(value: Any, name: str, allowed: set[str]) -> str:
    value = text(value, name)
    if value not in allowed:
        raise ValueError(f"{name} must be one of {', '.join(sorted(allowed))}")
    return value


def http_url(value: Any, name: str = "url") -> str:
    value = text(value, name)
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or any(c.isspace() for c in value):
        raise ValueError(f"{name} must be a complete HTTP(S) URL")
    return value


def handle(value: Any) -> str:
    value = text(value, "screenname").removeprefix("@")
    if not re.fullmatch(r"[A-Za-z0-9_]{1,15}", value):
        raise ValueError("screenname must be an X handle of 1-15 letters, digits or underscores")
    return value


def object_list(value: Any, name: str, *, allow_none: bool = False) -> list[dict[str, Any]]:
    if value is None and allow_none:
        return []
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValueError(f"{name} must be a list of objects")
    return value


def arxiv_id(value: Any) -> str:
    value = text(value, "arxiv_url")
    if "://" in value:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or parsed.hostname not in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}:
            raise ValueError("Expected an arXiv ID or arxiv.org URL")
        value = parsed.path
        if value.startswith("/abs/"):
            value = value[5:]
        elif value.startswith("/pdf/"):
            value = value[5:]
        else:
            raise ValueError("Expected an arXiv abstract or PDF URL")
    value = value.removesuffix(".pdf")
    if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[A-Za-z][A-Za-z.\-]*/\d{7})(?:v[1-9]\d*)?", value):
        raise ValueError("Invalid arXiv ID or URL")
    return value
