from celery import Celery
from config import REDIS_USER, REDIS_PASSWORD


app = Celery(
    'autoyarmarok',
    broker=f"redis://{REDIS_USER}:{REDIS_PASSWORD}@redis:6379/0",
    include=['src.tasks']
)
app.autodiscover_tasks()
