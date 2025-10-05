import os

from celery import Celery

connection_string = (
    f"redis://{os.environ['REDIS_USER']}:{os.environ['REDIS_PASSWORD']}"
    f"@{os.environ['REDIS_HOST']}:{os.environ['REDIS_PORT']}/"
)
celery_app = Celery(
    "worker",
    broker=f"{connection_string}{int(os.environ['REDIS_DB']) + 1}",
    backend=f"{connection_string}{int(os.environ['REDIS_DB']) + 2}",
)
celery_app.autodiscover_tasks()
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Moscow",
    enable_utc=False,
)
