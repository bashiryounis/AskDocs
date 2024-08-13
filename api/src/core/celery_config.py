from celery import Celery
from src.core.db import REDIS_URL
celery_app = Celery(
    'chat_service',
    broker='redis://redis:6379/0',  # Redis database 0 for the broker
    backend='redis://redis:6379/0',  # Redis database 0 for the backend
    include=['src.services.chat.background_tasks']  # Include your tasks module
)

celery_app.conf.update(
    result_expires=3600,  # Results expiration time
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
