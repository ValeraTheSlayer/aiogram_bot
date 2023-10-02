from celery import Celery

app = Celery('myapp')
app.config_from_object('celery_config')
