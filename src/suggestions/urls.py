from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.suggestion_view, name='suggestion'),
]