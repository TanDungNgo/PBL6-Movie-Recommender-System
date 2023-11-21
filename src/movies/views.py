from typing import Any
from django.db import models
from django.shortcuts import render
from django.views import generic
from django.db.models import Avg
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Movie
import requests
# Create your views here.
class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 100
    # context -> object_list
    queryset = Movie.objects.all().order_by('-rating_avg')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        requests = self.request
        user = requests.user
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list][:20]
            my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context['my_ratings'] = my_ratings
        return context



movie_list_view = MovieListView.as_view()
class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_requests = self.request  # Rename 'requests' to 'movie_requests'
        user = movie_requests.user
        if user.is_authenticated:
            movie_object = context['object']
            object_ids = [movie_object.id]
            my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            
            context['my_ratings'] = my_ratings

        movies = Movie.objects.all().order_by('-rating_avg')
        # Retrieve the movie_id from URL parameters or self.kwargs
        movie_id = self.kwargs.get('pk')  # Assuming your URL pattern uses 'pk' for the movie ID

        top_rated_movies = Movie.objects.all().order_by('-rating_avg')[:20]

        # Lấy danh sách diễn viên, đạo diễn
        url_credits = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url_credits)
        response.raise_for_status()
        data = response.json()
        casts = data.get('cast', [])[:8]
        directors = [crew for crew in data.get('crew', []) if crew.get('job') == 'Director']

        num_casts_per_row = len(casts) // 2
        first_row = casts[:num_casts_per_row]
        second_row = casts[num_casts_per_row:]

        # Lấy danh sách thể loại
        url_movie = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url_movie)
        response.raise_for_status()
        data_movie = response.json()
        genres = data_movie.get('genres', [])
        countries = data_movie.get('production_countries', [])
        poster_path = data_movie.get('poster_path', [])

        context['top_rated_movies'] = top_rated_movies
        context.update({
            'movie_id': movie_id,
            'casts': casts,
            'first_row': first_row,
            'second_row': second_row,
            'genres': genres,
            'countries': countries,
            'directors': directors,
            'poster_path': poster_path,
        })

        return context

movie_detail_view = MovieDetailView.as_view()


class Home(generic.ListView):
    template_name = 'dpthome/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Movie.objects.order_by('-release_date')[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_rated_movies'] = Movie.objects.order_by('-rating_avg')[:20]
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
    
        