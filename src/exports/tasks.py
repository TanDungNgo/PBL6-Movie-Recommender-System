from celery import shared_task

from . import utils as export_utils

@shared_task(name='export_rating_dataset')
def export_rating_dataset():
    export_utils.generate_rating_dataset(to_csv=True)


@shared_task(name='export_movie_dataset')
def export_movie_dataset():
    export_utils.generate_movies_dataset(to_csv=True)