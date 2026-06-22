from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

from app.db.models import Source


def scrape_html(source: Source) -> list[dict]:

    response = httpx.get(source.url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for tag in soup.find_all("article"):
        title_tag = tag.find(["h1", "h2", "h3", "a"])
        if not title_tag:
            continue
        items.append({
            "title": title_tag.get_text(strip=True),
            "url": title_tag.get("href"),
            "summary": tag.get_text(strip=True)[:300],
            "source": source.name,
            "published_at": datetime.now(timezone.utc),
            "raw_text": tag.get_text(strip=True),
        }
        )
    return items
