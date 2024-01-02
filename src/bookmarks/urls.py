from django.urls import path
from .views import toggle_bookmark, bookmarked_movies, get_bookmarked_user_ids

urlpatterns = [
    path('movie/', toggle_bookmark, name='toggle_bookmark'),
    path('movies/', bookmarked_movies, name='bookmarked_movies'),
    path('get_bookmarked_user_ids/', get_bookmarked_user_ids, name='get_bookmarked_user_ids')
]