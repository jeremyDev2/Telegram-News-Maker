import asyncio

from sqlalchemy import select

from app.db.models import NewsItem, Source
from app.db.enums import SourceType
from app.db.session import session_factory
from app.news_parser.sources.sites.sites import parse_site
from app.news_parser.sources.tg.telegram_groups import get_messages
from app.workers.celery_app import celery_app

async def _collect_sites() -> list[str]:
    
    async with session_factory() as session:
        
        result = await session.execute(select(Source).where(Source.type == SourceType.SITE, Source.enabled ==True))
        sources = result.scalars().all()

        ids = []

        for source in sources:
            for item in parse_site(source):
                news = NewsItem(**item)
                session.add(news)
                await session.flush()
                ids.append(str(news.id))
        await session.commit()
        return ids

@celery_app.task(name="collect.sites")
def collect_news_sites() -> list[str]:
    return asyncio.run(_collect_sites())

async def _collect_telegram() -> list[str]:

    async with session_factory() as session: 

        result = await session.execute(select(Source).where(Source.type == SourceType.TG, Source.enabled == True))
        sources = result.scalars().all()

        ids = []

        for source in sources:
            for item in await get_messages(source):
                news = NewsItem(**item)
                session.add(news)
                await session.flush()
                ids.append(str(news.id))
        await session.commit()
        return ids

@celery_app.task(name="collect.tg")
def collect_news_telegram() -> list[str]:
    return asyncio.run(_collect_telegram())
