from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err
from tools._validation import text as validate_text


def send_telegram(text: str = "", confirmed: bool = False) -> dict[str, Any]:
    if confirmed is not True:
        return {
            "tool": "send_telegram",
            "status": "needs_confirmation",
            "message": "Only send after the user explicitly confirms.",
        }
    try:
        text = validate_text(text, "text")
        if len(text) > 4096:
            raise ValueError("Telegram text must be at most 4096 characters")
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if not token or not chat_id:
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID env var")
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
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

