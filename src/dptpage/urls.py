from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog_detai/', views.blog_detail, name='blog_detail'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('search_page/', views.search_page, name='search_page'),
    path('page_not_found/', views.page_not_found, name='page_not_found'),
]