from __future__ import annotations

from typing import Any

from tools._shared import err
from tools._validation import choice, text


def ask_user(
    question: str = "",
    response_type: str = "text",
    options: list[str] | None = None,
    draft: str | None = None,
    destination: str | None = None,
) -> dict[str, Any]:
    try:
        question = text(question, "question")
        response_type = choice(response_type, "response_type", {"text", "yes_no", "choice"})
        options = [] if options is None else options
        if not isinstance(options, list) or any(not isinstance(item, str) or not item.strip() for item in options):
            raise ValueError("options must be a list of non-empty strings")
        if response_type == "choice" and len(options) < 2:
            raise ValueError("choice requires at least two options")
        if draft is not None:
            draft = text(draft, "draft")
        if destination is not None:
            destination = text(destination, "destination")
        return {
            "tool": "ask_user",
            "question": question,
            "response_type": response_type,
            "options": list(options),
            "awaiting_user": True,
            "draft": draft,
            "destination": destination,
        }
    except Exception as exc:
        return err("ask_user", exc)
