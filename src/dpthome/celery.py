import os

from celery import Celery
from celery.schedules import crontab

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
        'schedule': 60 * 30, # 30 min,
    },
    "run_rating_export_every_hour": {
        'task': 'export_rating_dataset',
        'schedule': crontab(hour=1, minute=30),
    },
    "run_movie_export_every_hour": {
        'task': 'export_movie_dataset',
        'schedule': crontab(hour=2, minute=15),
    },
    "daily_train_model": {
        'task': 'train_model_task',
        'schedule': crontab(hour=4, minute=0),
    },
    "daily_batch_users_prediction": {
        'task': 'batch_users_prediction_task',
        'schedule': crontab(hour=5, minute=0),
    },
    "daily_movie_idx_refresh":{
        'task': 'task_update_movie_position_embedding_idx',
        'schedule': crontab(hour=2, minute=0),
    }
}