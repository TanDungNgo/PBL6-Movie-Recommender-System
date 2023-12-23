from django.apps import apps
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.utils import timezone
from profiles.models import CustomUser as User


# Create your models here.
# User = settings.AUTH_USER_MODEL # 'auth.User'


class ReviewQuerySet(models.QuerySet):
    def as_object_dict(self, object_ids=[]):
        # Correct the filter syntax here
        qs = self.filter(object_id__in=object_ids)
        return {f"{x.object_id}": x.value for x in qs}

    def movies(self):
        Movie = apps.get_model('movies', 'Movie')
        ctype = ContentType.objects.get_for_model(Movie)
        return self.filter(active=True, content_type=ctype)

class RatingManager(models.Manager):
    def get_queryset(self):
        return ReviewQuerySet(self.model, using=self._db)
    
    def movies(self):
        return self.get_queryset().movies()
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type","object_id")
    active = models.BooleanField(default=True)
    active_update_timestamp = models.DateTimeField(auto_now_add=False,
                                                   auto_now=False,null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']