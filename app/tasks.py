from app.models import ScheduledMessage
from datetime import datetime

from celery_app import app
from main import bot


@app.task
def send_scheduled_messages():
    now = datetime.now()
    for scheduled_message in ScheduledMessage.select().where(ScheduledMessage.send_at <= now):
        template = scheduled_message.template
        user_id = scheduled_message.user.user_id

        if template.content:
            bot.send_message(chat_id=user_id, text=template.content)
        if template.image:
            bot.send_photo(chat_id=user_id, photo=template.image)
        if template.video:
            bot.send_video(chat_id=user_id, video=template.video)

        scheduled_message.delete_instance()
