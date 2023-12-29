from django.db import models
from profiles.models import CustomUser as User
from movies.models import Movie

# Create your models here.
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    active_update_timestamp = models.DateTimeField(auto_now_add=False,
                                                   auto_now=False,null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] 