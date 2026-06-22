from datetime import datetime, timezone

import feedparser
from dateutil import parser as date_parser

from app.db.models import Source

def _entry_to_dict(entry, source: Source) -> dict:

    published_raw = entry.get("published") or entry.get("updated")
    try:
        published_at = date_parser.parse(published_raw) if published_raw else datetime.now(timezone.utc)
    except (ValueError, TypeError):
        published_at = datetime.now(timezone.utc)
    return {
        "title": entry.get("title", ""),
        "url": entry.get("link"),
        "summary": entry.get("summary", ""),
        "source": source.name,
        "published_at": published_at,
        "raw_text": entry.get("summary", ""),
    }

def get_rss(source: Source) -> list[dict]:

    feed = feedparser.parse(source.url)
    if not feed.entries:
        return []
    return [_entry_to_dict(entry, source) for entry in feed.entries]
