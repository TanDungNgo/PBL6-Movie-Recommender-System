from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.movie_list_view),
    path('movies/<int:pk>/', views.movie_detail_view, name='movie_detail'),
    path('movies/<int:pk>/video/', views.movie_video_view),
    path('movies/find/', views.search_movie, name='movie_find_view'),
    path('movies/recommend/<int:pk>/', views.get_recommendations, name='movie_recommend_view'),
]