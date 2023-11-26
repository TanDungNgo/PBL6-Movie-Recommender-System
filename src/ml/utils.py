import pickle
import tempfile

from django.core.files.base import File
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.conf import settings

from ratings.models import Rating

def export_dataset():
    ctype = ContentType.objects.get(app_label='movies', model='movie')
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(
        user_id=F('user__id'),
        movie_id=F('object_id'),
        rating=F('value'),
    )
    return qs.values('user_id', 'movie_id', 'rating')


def train_model():
    pass


def export_model():
    pass


def load_model():
    pass