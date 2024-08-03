from celery import Celery
from celery.schedules import crontab
from config import REDIS_USER, REDIS_PASSWORD


app = Celery(
    'autoyarmarok',
    broker=f"redis://{REDIS_USER}:{REDIS_PASSWORD}@redis:6379/0",
    include=['worker.tasks']
)
app.conf.timezone = 'UTC+2'
app.conf.beat_schedule = {
    'prolongation_advertisement_question': {
        'task': 'worker.tasks.prolongation_advertisement_question',
        'schedule': crontab(minute='0', hour='9'),
    },
}
# app.autodiscover_tasks()
