from datetime import timedelta

from rapidfuzz import fuzz
from sqlalchemy import select

from app.db.models import Keyword, NewsItem
from app.db.session import session_factory
from app.workers.celery_app import celery_app

# fuzzy-match score (0-100) above which two titles count as the same news
DUPLICATE_THRESHOLD = 85

async def _matches_keywords(news: NewsItem, keywords: list[str]) -> bool:
    # no keywords configured means no filtering, everything passes
    if not keywords:
        return True
    haystack = f"{news.title} {news.raw_text}".lower()
    return any(word in haystack for word in keywords)

async def _is_duplicate(session, news: NewsItem) -> bool:
    # compare against news from the last day, skip the row itself
    recent = await session.execute(select(NewsItem)
                                   .where(NewsItem.published_at >= news.published_at - timedelta(days=1), NewsItem.id != news.id,))
    for existing in recent.scalars().all():
        if fuzz.ratio(news.title, existing.title) >= DUPLICATE_THRESHOLD:
            return True
    return False

async def _filter_and_dedup(news_ids: list[str]) -> list[str]:
    async with session_factory() as session:
        keywords_result = await session.execute(select(Keyword.word))
        keywords = [w.lower() for w in keywords_result.scalars().all()]

        kept_ids = []
        for news_id in news_ids:
            news = await session.get(NewsItem, news_id)
            # drop news that mention none of the configured keywords
            if not await _matches_keywords(news, keywords):
                continue
            # drop near-duplicate news already collected recently
            if await _is_duplicate(session, news):
                continue
            kept_ids.append(news_id)
        return kept_ids

@celery_app.task(name="filter.dedup")
def filter_and_dedup(news_ids: list[str]) -> list[str]:
    import asyncio
    return asyncio.run(_filter_and_dedup(news_ids))
