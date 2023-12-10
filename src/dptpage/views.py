from typing import Any
from django.db import models
from django.shortcuts import render
from django.views import generic
from django.db.models import Avg
from django.contrib.auth import get_user_model
import requests

User = get_user_model()
from movies.models import Movie

class Home(generic.ListView):
    template_name = 'dpthome/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Movie.objects.order_by('-release_date')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_rated_movies'] = Movie.objects.order_by('-score')[:20]
        context['latest_movies'] = self.get_queryset()
        return context

home = Home.as_view()


def about(request):
    return render(request, 'dpthome/about.html')
def blog(request):
    return render(request, 'dpthome/blog.html')
def blog_detail(request):
    return render(request, 'dpthome/blog_detail.html')
def services(request):
    return render(request, 'dpthome/services.html')
def contact(request):
    return render(request, 'dpthome/contact.html')
def search_page(request):
    return render(request, 'dpthome/search_page.html')
    
    

