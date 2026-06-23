from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup

from app.db.models import Source


def scrape_html(source: Source) -> list[dict]:

    headers = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}
    response = httpx.get(source.url, timeout=10, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    tags = soup.find_all("article")
    if not tags:
        tags = soup.find_all("div", class_=lambda c: c and "article_news_list" in c)

    for tag in tags:
        title_tag = tag.find(["h1", "h2", "h3", "a"], class_="article_title") or tag.find(["h1", "h2", "h3", "a"])
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
