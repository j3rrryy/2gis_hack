import os

import uvloop
from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from di import ClientSessionManager, SessionManager

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


@worker_process_init.connect
def init_worker(**kwargs):
    async def setup():
        await SessionManager.setup()
        await ClientSessionManager.setup()

    uvloop.run(setup())


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    async def cleanup():
        await ClientSessionManager.close()
        await SessionManager.close()

    uvloop.run(cleanup())
