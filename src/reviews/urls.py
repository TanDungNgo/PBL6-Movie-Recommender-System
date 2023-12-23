from django.urls import path
from . import views

urlpatterns = [
    path('review/movie/', views.review_movie, name='review_movie'),
    path('load-more-reviews/', views.load_more_reviews, name='load_more_reviews'),
    path('review/delete/', views.delete_review, name='delete_review'),
    path('review/update/', views.update_review, name='update_review'),
]