from django.urls import path
from .views import add_review

urlpatterns = [
    path('movies/<int:pk>/add_review/', add_review, name='add_review'),
]