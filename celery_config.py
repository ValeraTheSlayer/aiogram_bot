from datetime import timedelta

BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_BEAT_SCHEDULE = {
    'send_scheduled_messages': {
        'task': 'app.tasks.send_scheduled_messages',
        'schedule': timedelta(minutes=1),
    },
}
