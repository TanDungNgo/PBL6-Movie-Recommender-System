from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.movie_list_view),
    path('movies/<int:pk>/', views.movie_detail_view),
    path('movies/<int:pk>/video/', views.movie_video_view),
    path('movies/find/', views.movie_find_view, name='movie_find_view'),
]