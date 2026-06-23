from celery import chain, chord

from app.workers.celery_app import celery_app
from app.workers.tasks.collect import collect_news_sites, collect_news_telegram
from app.workers.tasks.filter import filter_and_dedup
from app.workers.tasks.generate import generate_post_task
from app.workers.tasks.publish import publish_post_task

@celery_app.task(name="pipeline.merge_collected")
def merge_collected(collected: list[list[str]]) -> list[str]:
    #chord callback receives one list per task in the group, flatten into one
    return [news_id for ids in collected for news_id in ids]

@celery_app.task(name="pipeline.run")
def run_pipeline() -> None:
    chord(
        [collect_news_sites.s(), collect_news_telegram.s()],
        chain(
            merge_collected.s(),
            filter_and_dedup.s(),
            generate_post_task.s(),
            publish_post_task.s(),
        ),
    ).delay()
