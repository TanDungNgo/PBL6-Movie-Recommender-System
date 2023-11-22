from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_movie, name='create_movie'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('user_list/', views.user_list, name='user_list'),
    path('export_movies/', views.export_movies, name='export_movies'),
    path('export_users/', views.export_users, name='export_users'),
    path('movie_list/<int:movie_id>/', views.movie_detail_admin, name='movie_detail_admin'),
    path('movie_list/edit/<int:movie_id>/', views.movie_edit, name='movie_edit'),
    path('movie_list/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('user_list/delete/<int:user_id>/', views.delete_user, name='delete_user'),
]