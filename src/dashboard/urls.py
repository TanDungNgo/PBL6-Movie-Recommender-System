from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_movie, name='create_movie'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('user_list/', views.get_list_users, name='user_list'),
    path('export_movies/', views.export_movies, name='export_movies'),
    path('print_movies/', views.print_movies, name='print_movies'),
    path('export_users/', views.export_users, name='export_users'),
    path('movie_list/<int:movie_id>/', views.movie_detail_admin, name='movie_detail_admin'),
    path('movie_list/edit/<int:movie_id>/', views.edit_movie, name='movie_edit'),
    path('movie_list/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('user_list/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_by_month/', views.users_by_month, name='users_by_month'),
    path('movies_by_genre/', views.movies_by_genre, name='movies_by_genre'),
    path('rating_review/', views.get_movie_review_counts, name='rating_review'),
    path('rating_review/reviews/<int:movie_id>/', views.get_movie_review_details, name='review_details'),
    path('rating_review/ratings/<int:movie_id>/', views.get_movie_rating_details, name='rating_details'),
    path('rating_review/ratings/<int:movie_id>/rating_count/', views.get_rating_count, name='rating_count'),
    path('export_models/', views.get_export_model_list, name='export_models'),
    path('train_model/', views.train_model, name='train_model'),
    path('trigger_batch_users_prediction/', views.batch_users_prediction, name='predict_model'),
    path('update_rating_avg/', views.update_rating_avg, name='update_rating_avg'),
]