from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

from tools._shared import TIMEOUT, err
from tools._validation import text as validate_text


@dataclass(frozen=True)
class _SendApproval:
    text: str
    destination: str


def _approve_send_after_user_confirmation(text: str, destination: str) -> _SendApproval:
    return _SendApproval(text=text, destination=destination)


def send_telegram(
    text: str = "",
    confirmed: bool = False,
    destination: str | None = None,
    *,
    approval: _SendApproval | None = None,
) -> dict[str, Any]:
    try:
        text = validate_text(text, "text")
        if len(text) > 4096:
            raise ValueError("Telegram text must be at most 4096 characters")
    except Exception as exc:
        return err("send_telegram", exc)

    destination = destination or os.getenv("TELEGRAM_CHAT_ID")
    if not destination:
        return {
            "tool": "send_telegram",
            "status": "needs_destination",
            "draft": text,
            "message": "A Telegram destination is required before this message can be sent.",
        }
    try:
        destination = validate_text(destination, "destination")
        if any(character.isspace() for character in destination):
            raise ValueError("destination must be a Telegram chat ID or channel username without spaces")
    except Exception as exc:
        return err("send_telegram", exc)

    if (
        confirmed is not True
        or not isinstance(approval, _SendApproval)
        or approval.text != text
        or approval.destination != destination
    ):
        return {
            "tool": "send_telegram",
            "status": "needs_confirmation",
            "draft": text,
            "destination": destination,
            "message": "Show this exact draft and destination and wait for explicit user approval.",
        }

    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var")
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": destination, "text": text, "parse_mode": "Markdown"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("ok") is not True:
            raise RuntimeError("Telegram reported an unsuccessful send")
        return {"tool": "send_telegram", "status": "sent"}
    except Exception as exc:
        result = err("send_telegram", exc)
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if token:
            result["message"] = result["message"].replace(token, "[redacted]")
        return result
