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
        print('Found', len(users_ids), 'users')
        print('Predicting for users', users_ids)
    
    # movie_ids = list(Movie.objects.filter(id__lt=42008).popular().values_list('id', flat=True)[start_page:end_page])
    movie_ids = list(Movie.objects.all().popular().values_list('idx', flat=True)[start_page:end_page])
    print('Found', len(movie_ids), 'movies')
    print('Predicting for movies', movie_ids)
    recently_suggested = Suggestion.objects.get_recently_suggested(movie_ids, users_ids)
    
    for user_id in users_ids:
        user_list = [user_id] * len(movie_ids)        
        print('Predicting for user', user_id)
        print('Length of user list', len(user_list))
        print('Length of movie list', len(movie_ids))
        preds = model.predict(x=[np.array(user_list), np.array(movie_ids)])
        print('Predictions', preds)
        for i, movie_id in enumerate(movie_ids):
            pred_rank = preds[i][0]
            data = {
                'user_id': user_id,
                'object_id': movie_id,
                'content_type': ctype,
                'value': pred_rank,
            }
            
            try:
                print('Predicted rank for movie', movie_id, 'is', pred_rank)
                obj, created = Suggestion.objects.get_or_create(user_id=user_id, object_id=movie_id, content_type=ctype)
            except Suggestion.MultipleObjectsReturned:
                print('Multiple objects returned for user', user_id, 'and movie', movie_id)
                qs = Suggestion.objects.filter(user_id=user_id, object_id=movie_id, content_type=ctype)
                obj = qs.first()
                to_delete = qs.exclude(id=obj.id)
                to_delete.delete()
            
            if not created and obj.value != pred_rank:
                print('Updating rank for movie', movie_id, 'for user', user_id, 'from', obj.value, 'to', pred_rank)
                obj.value = pred_rank
                obj.save()
    # if end_page < max_pages:
    #     return batch_users_prediction_task(start_page=end_page-1)