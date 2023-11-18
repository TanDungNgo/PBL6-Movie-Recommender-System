import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dpthome.settings')

app = Celery('dpthome')

# CELERY_
app.config_from_object("django.conf:settings", namespace='CELERY')

# app.conf.broker_url = ''
# app.conf.result_backend ='django-db'
app.autodiscover_tasks()

app.conf.beat_scheduler = {
    "run_movie_rating_avg_every_30": {
        'task': 'task_update_movie_ratings',
        'schedule': 5.0,
        'kwargs': {"all": True},
    },
}