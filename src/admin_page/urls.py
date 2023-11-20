from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view),
    path('movies/', views.movie_list_view),
    path('users/', views.user_list_view),
    path('create_movie/', views.movie_create_view),
]