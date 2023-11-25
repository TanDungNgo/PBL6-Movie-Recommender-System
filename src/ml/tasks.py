from celery import shared_task

from . import utils as ml_utils
from profiles import utils as profile_utils
from movies.models import Movie

@shared_task(name='train_model_task')
def train_model_task():
    ml_utils.train_model()


@shared_task(name='')
def batch_user_prediction_task():
    model = ml_utils.load_model()
    recent_user_ids = profile_utils.get_recent_users()
    movie_ids = Movie.objects.all().popular().values_list('id', flat=True)
    return movie_ids