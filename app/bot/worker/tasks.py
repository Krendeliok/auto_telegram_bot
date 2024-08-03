from celery import shared_task
from main import bot


@shared_task
def prolongation_advertisement(telegram_id: int, advertisement_id: int):
    bot.send_message(telegram_id, 'Ваше объявление было продлено на 7 дней')
