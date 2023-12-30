from django.contrib import admin

# Register your models here.
from .models import Movie, Genre

class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'tmdb_id','display_genres','rating_count', 'rating_avg', 'score',
                    'rating_last_updated']
    readonly_fields = ['idx','rating_avg', 'rating_count']
    search_fields = ['title']
    def display_genres(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

    display_genres.short_description = 'Genres'

class GenreAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    search_fields = ['name']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)