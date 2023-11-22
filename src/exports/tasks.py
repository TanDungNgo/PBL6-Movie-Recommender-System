from celery import shared_task

from . import utils as export_utils

@shared_task(name='export_rating_dataset')
def export_rating_dataset():
    export_utils.export_dataset()