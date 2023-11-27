from celery import shared_task
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from . import utils as ml_utils
from profiles import utils as profile_utils
from movies.models import Movie
import numpy as np


@shared_task(name='train_model_task')
def train_model_task():
    ml_utils.train_model()


@shared_task(name='batch_users_prediction_task')
def batch_users_prediction_task(users_ids=None, start_page=0, offset=50, max_pages=1000):
    model = ml_utils.load_model_keras()
    Suggestion = apps.get_model('suggestions', 'Suggestion')
    ctype = ContentType.objects.get(app_label='movies', model='movie')
    
    end_page = start_page + offset
    
    if users_ids is None:
        users_ids = profile_utils.get_recent_users_ratings()
    
    movie_ids = list(Movie.objects.filter(id__lt=42008).popular().values_list('id', flat=True)[start_page:end_page])
    recently_suggested = Suggestion.objects.get_recently_suggested(movie_ids, users_ids)
    
    for user_id in users_ids:
        user_list = [user_id] * len(movie_ids)        
        print('Predicting for user', user_id)
        preds = model.predict(x=[np.array(user_list), np.array(movie_ids)])
        for i, movie_id in enumerate(movie_ids):
            pred_rank = preds[i][0]
            data = {
                'user_id': user_id,
                'object_id': movie_id,
                'content_type': ctype,
                'value': pred_rank,
            }
            
            try:
                obj, created = Suggestion.objects.get_or_create(user_id=user_id, object_id=movie_id, content_type=ctype)
                
            except Suggestion.MultipleObjectsReturned:
                qs = Suggestion.objects.filter(user_id=user_id, object_id=movie_id, content_type=ctype)
                obj = qs.first()
                to_delete = qs.exclude(id=obj.id)
                to_delete.delete()
            
            if not created and obj.value != pred_rank:
                obj.value = pred_rank
                obj.save()
    # if end_page < max_pages:
    #     return batch_users_prediction_task(start_page=end_page-1)