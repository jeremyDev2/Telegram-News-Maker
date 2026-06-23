import asyncio

from app.ai.generator import generate_post
from app.db.enums import PostStatus
from app.db.models import NewsItem, Post
from app.db.session import session_factory
from app.workers.celery_app import celery_app

async def _generate_post(news_ids: list[str]) -> list[str]:

    async with session_factory() as session:
        post_ids= []
        for news_id in news_ids:
            news = await session.get(NewsItem, news_id)
            generated_text = await generate_post(news.raw_text)

            post = Post(news_id = news.id, 
                        generated_text = generated_text, 
                        status=PostStatus.GENERATED
            )
            session.add(post)
            await session.flush()
            post_ids.append(str(post.id))
        await session.commit()
        return post_ids

@celery_app.task(name="generate.post")
def generate_post_task(news_ids: list[str]) -> list[str]:
    return asyncio.run(_generate_post(news_ids))
