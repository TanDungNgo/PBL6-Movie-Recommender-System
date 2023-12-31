from django.db import models
from django.utils import timezone
import uuid
import pathlib
from . import storages as exports_storages
# Create your models here.

def export_file_handler(instance, filename):
    today = timezone.now().strftime('%Y-%m-%d')
    fpath = pathlib.Path(filename)
    ext = fpath.suffix # get file extension .csv
    dtype = instance.type
    if hasattr(instance, 'id'):
        new_fname = f'{instance.id}{ext}'
    else:
        new_fname = f'{uuid.uuid4()}{ext}'
    return f'exports/{dtype}/{today}/{new_fname}'

class ExportDataType(models.TextChoices):
    RATINGS = 'ratings', 'Ratings'
    MOVIES = 'movies', 'Movies'

class Export(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=export_file_handler,blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=ExportDataType.choices, default=ExportDataType.RATINGS)
    latest = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.latest and self.file:
            file = self.file
            ext = pathlib.Path(file.name).suffix
            path = f"exports/{self.type}/latest{ext}"
            exports_storages.save(path, file, overwrite=True)
            qs = Export.objects.filter(type=self.type).exclude(pk=self.pk)
            qs.update(latest=False)

class ExportModelNCF(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.CharField(max_length=200, default='model')
    n_epochs = models.IntegerField(default=10)
    batch_size = models.IntegerField(default=200)
    learning_rate = models.FloatField(default=0.005)
    embedding_size = models.IntegerField(default=500)
    timestamp = models.DateTimeField(auto_now_add=True)