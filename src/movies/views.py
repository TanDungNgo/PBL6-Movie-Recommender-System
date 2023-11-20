from typing import Any
from django.db import models
from django.shortcuts import render
from django.views import generic
from django.db.models import Avg

from django.conf import settings
from .models import Movie
import requests
# Create your views here.
API_KEY = settings.API_KEY

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
        url_credits = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US'
        response = requests.get(url_credits)
        response.raise_for_status()
        data = response.json()
        casts = data.get('cast', [])[:8]
        directors = [crew for crew in data.get('crew', []) if crew.get('job') == 'Director']

        num_casts_per_row = len(casts) // 2
        first_row = casts[:num_casts_per_row]
        second_row = casts[num_casts_per_row:]

        # Lấy danh sách thể loại
        url_movie = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url_movie)
        response.raise_for_status()
        data_movie = response.json()
        genres = data_movie.get('genres', [])
        countries = data_movie.get('production_countries', [])

        context['top_rated_movies'] = top_rated_movies
        context.update({
            'movie_id': movie_id,
            'casts': casts,
            'first_row': first_row,
            'second_row': second_row,
            'genres': genres,
            'countries': countries,
            'directors': directors,
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

class MovieVideoView(generic.DetailView):
    model = Movie
    template_name = 'movies/watch_video.html'  # Tạo một template mới cho việc xem video
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('pk')
        url_movie = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US'
        response = requests.get(url_movie)
        response.raise_for_status()
        data_movie = response.json()
        context['key'] = data_movie.get("results", [])[0].get("key")
        return context

movie_video_view = MovieVideoView.as_view()
