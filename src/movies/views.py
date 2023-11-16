from django.shortcuts import render
from django.views import generic
from django.db.models import Avg

from .models import Movie
import requests
# Create your views here.
class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 10
    # context -> object_list
    queryset = Movie.objects.all().order_by('-release_date')[:20]

movie_list_view = MovieListView.as_view()
class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = Movie.objects.all().order_by('-rating_avg')
        # Retrieve the movie_id from URL parameters or self.kwargs
        movie_id = self.kwargs.get('pk')  # Assuming your URL pattern uses 'pk' for the movie ID

        top_rated_movies = Movie.objects.all().order_by('-rating_avg')[:10]

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