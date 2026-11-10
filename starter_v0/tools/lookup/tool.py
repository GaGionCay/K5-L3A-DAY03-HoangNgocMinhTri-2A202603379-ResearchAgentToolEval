from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err
from tools._validation import choice, integer, object_list, text


def web_search(query: str = "", topic: str = "general", timeframe: str | None = "week", max_results: int = 5) -> dict[str, Any]:
    try:
        query = text(query, "query")
        topic = choice(topic, "topic", {"general", "news"})
        if timeframe is not None:
            timeframe = choice(timeframe, "timeframe", {"day", "week", "month", "year"})
        max_results = integer(max_results, "max_results", maximum=20)
        key = os.getenv("TAVILY_API_KEY")
        if not key:
            raise RuntimeError("Missing TAVILY_API_KEY env var")
        body: dict[str, Any] = {"query": query, "topic": topic, "max_results": max_results, "search_depth": "basic"}
        if timeframe:
            body["time_range"] = timeframe
        response = requests.post(
            "https://api.tavily.com/search",
            json=body,
            headers={"Authorization": f"Bearer {key}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        items = [{
            "title": item.get("title"),
            "url": item.get("url"),
            "source": domain(item.get("url", "")),
            "summary": item.get("content"),
            "score": item.get("score"),
        } for item in object_list(data.get("results", []), "results")[:max_results]]
        return {"tool": "web_search", "query": query, "topic": topic, "timeframe": timeframe, "items": items}
    except Exception as exc:
        return err("web_search", exc)

