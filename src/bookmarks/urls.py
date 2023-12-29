from django.urls import path
from .views import toggle_bookmark, bookmarked_movies

urlpatterns = [
    path('movie/', toggle_bookmark, name='toggle_bookmark'),
    path('movies/', bookmarked_movies, name='bookmarked_movies'),
]