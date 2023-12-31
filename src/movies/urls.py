from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list_view, name='movies'),
    path('movies/<int:pk>/', views.movie_detail_view, name='movie_detail'),
    path('movies/<int:pk>/video/', views.movie_video_view),
    path('movies/find/', views.search_movie, name='movie_find_view'),
    path('movies/recommend/<int:pk>/', views.get_recommendations, name='movie_recommend_view'),
    path('myrating/movies/', views.get_my_ratings, name='myrating_movies'),
    path('filter/movies/', views.get_filtered_movies, name='filter_movies'),
    path('movies/cast/', views.get_movies_by_cast, name='get_movies_by_cast'),

]
