from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, domain, err
from tools._validation import choice, integer, object_list, text
from time_context import current_time_context


def web_search(query: str = "", topic: str = "general", timeframe: str | None = None, max_results: int = 5, max_age_hours: int | None = None) -> dict[str, Any]:
    try:
        query = text(query, "query")
        topic = choice(topic, "topic", {"general", "news"})
        if timeframe is not None:
            timeframe = choice(timeframe, "timeframe", {"day", "week", "month", "year"})
        max_results = integer(max_results, "max_results", maximum=20)
        if max_age_hours is not None:
            max_age_hours = integer(max_age_hours, "max_age_hours", minimum=0, maximum=720)
        key = os.getenv("TAVILY_API_KEY")
        if not key:
            raise RuntimeError("Missing TAVILY_API_KEY env var")
        body: dict[str, Any] = {
            "query": query, "topic": topic, "max_results": max_results,
            "search_depth": "basic", "include_published_date": True,
        }
        if timeframe:
            body["time_range"] = timeframe
        if max_age_hours is not None:
            body["max_age_hours"] = max_age_hours
        response = requests.post(
            "https://api.tavily.com/search",
            json=body,
            headers={"Authorization": f"Bearer {key}"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        items = []
        for item in object_list(data.get("results", []), "results")[:max_results]:
            mapped = {
                "title": item.get("title"), "url": item.get("url"),
                "source": domain(item.get("url", "")), "summary": item.get("content"),
                "score": item.get("score"),
            }
            if item.get("published_date") is not None:
                mapped["published_date"] = item["published_date"]
            items.append(mapped)
        return {
            "tool": "web_search", "query": query, "topic": topic,
            "timeframe": timeframe, "max_age_hours": max_age_hours,
            "retrieved_at": current_time_context()["current_datetime"], "items": items,
        }
    except Exception as exc:
        return err("web_search", exc)

