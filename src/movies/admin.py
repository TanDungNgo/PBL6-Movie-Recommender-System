from django.contrib import admin

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'rating_count', 'rating_avg',
                    'rating_last_updated']
    readonly_fields = ['rating_avg', 'rating_count']
    search_fields = ['title']

admin.site.register(Movie, MovieAdmin) 