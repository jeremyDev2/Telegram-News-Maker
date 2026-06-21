from celery import Celery
from app.config import settings

celery_app = Celery(

    "telegram_news_maker",
    #task queue where Celery contain task and worker take this task
    broker=settings.CELERY_BROKER_URL,
    #place whith task's result's
    backend=settings.CELERY_RESULT_BACKEND,

)
