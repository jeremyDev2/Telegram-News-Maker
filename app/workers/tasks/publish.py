import asyncio
from datetime import datetime, timezone

from app.db.enums import PostStatus
from app.db.models import Post
from app.db.session import session_factory
from app.telegram.publisher import publish_post
from app.workers.celery_app import celery_app


async def _publish_post(post_ids: list[str]) -> list[str]:
    async with session_factory() as session:
        published_ids = []
        for post_id in post_ids: 
            post = await session.get(Post, post_id)
            success = await publish_post(post)

            if success:
                post.status = PostStatus.PUBLISHED
                post.published_at = datetime.now(timezone.utc)
                published_ids.append(post_id)
            else:
                post.status = PostStatus.FAILED

        await session.commit()
        return published_ids

@celery_app.task(name="publish.post")
def publish_post_task(post_ids: list[str]) -> list[str]:
    return asyncio.run(_publish_post(post_ids))
