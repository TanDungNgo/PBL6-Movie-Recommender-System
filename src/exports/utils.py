import csv
import tempfile
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.core.files import File

from movies.models import Movie
from ratings.models import Rating

from .models import Export, ExportDataType


def export_dataset(dataset, fname='dataset.csv', type=ExportDataType.RATINGS):
    with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', newline='') as temp_f:
        try:
            keys = dataset[0].keys()
        except:
            return
        dict_writer = csv.DictWriter(temp_f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dataset)
        temp_f.seek(0)  # Đưa con trỏ về đầu tệp
        # Ghi đối tượng Export
        obj = Export.objects.create(type=type)
        obj.file.save(fname, File(temp_f))

def generate_rating_dataset(app_label='movies', model='movie', to_csv=True):
    ctype = ContentType.objects.get(app_label=app_label, model=model)
    qs = Rating.objects.filter(active=True, content_type=ctype)
    qs = qs.annotate(userId=F('user_id'), movieId=F('object_id'), rating=F('value'))
    dataset = qs.values('userId', 'movieId', 'rating')
    if to_csv:
        export_dataset(dataset=dataset, fname='ratings.csv', type=ExportDataType.RATINGS)
    return dataset

def generate_movies_dataset(to_csv=True):
    qs = Movie.objects.all()
    qs = qs.annotate(movieId=F('id'), movieIdx=F("idx"))
    dataset = qs.values('movieIdx', 'movieId', 'release_date', 'rating_count', 'rating_avg')
    if to_csv:
        export_dataset(dataset=dataset, fname='movies.csv', type=ExportDataType.MOVIES)
    return dataset

