"""Supply the current Vietnam date at runtime; never hard-code today's date."""
from datetime import datetime, timedelta, timezone


VIETNAM_TIMEZONE = timezone(timedelta(hours=7), name="Asia/Ho_Chi_Minh")


def current_time_context(now: datetime | None = None) -> dict[str, str]:
    now = datetime.now(timezone.utc) if now is None else now
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must include a timezone")
    local = now.astimezone(VIETNAM_TIMEZONE)
    return {
        "current_datetime": local.isoformat(timespec="seconds"),
        "current_date": local.date().isoformat(),
        "display_date": local.strftime("%d/%m/%Y"),
        "timezone": "Asia/Ho_Chi_Minh",
        "utc_offset": "+07:00",
    }


def time_context_message(context: dict[str, str]) -> dict[str, str]:
    return {
        "role": "system",
        "content": (
            f"Current local date from the application clock: {context['current_date']} "
            f"({context['display_date']}). Current local time: {context['current_datetime']}. "
            "User timezone: Asia/Ho_Chi_Minh (UTC+07:00). Resolve 'today' and 'hôm nay' "
            "against this date, not an article date, model memory or an earlier answer. "
            "Honor a different historical date only when the user explicitly requests it. "
            "For today's news use lookup(topic='news', timeframe='day'). "
            "For current prices, exchange rates or weather, search a date-specific query with "
            "lookup(topic='general', max_age_hours=0), omitting timeframe so continuously "
            "updated pages are not excluded because of old publication dates. "
            "Use live tool results before stating current values. Check each source's date "
            "and the time the quoted value applies to. published_date is a provider estimate "
            "of publication/update time; retrieved_at is only when we fetched the result. "
            "Neither alone proves a price is current. If the source is old or its as-of time "
            "cannot be verified, state that limitation and do not label it as today's value. "
            "Never relabel an older quote with today's date or invent a timestamp."
        ),
    }
