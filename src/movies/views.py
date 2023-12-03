
from django.shortcuts import render
from django.views import generic
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()

from django.conf import settings

from django.conf import settings
from .models import Movie
import requests
# Create your views here.
API_KEY = settings.API_KEY

class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 100
    # context -> object_list
    queryset = Movie.objects.all().order_by('-score')

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
        movie = Movie.objects.get(pk=movie_id)
        top_rated_movies = Movie.objects.all().order_by('-score')[:20]
        related_movies = Movie.objects.filter(title__icontains=movie.title).exclude(id=movie.id)[:20]

        # Lấy danh sách diễn viên, đạo diễn
        url_credits = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/credits?api_key={API_KEY}&language=en-US'
        response = requests.get(url_credits)
        response.raise_for_status()
        data = response.json()
        casts = data.get('cast', [])[:8]
        directors = [crew for crew in data.get('crew', []) if crew.get('job') == 'Director']

        num_casts_per_row = len(casts) // 2
        first_row = casts[:num_casts_per_row]
        second_row = casts[num_casts_per_row:]

        # Lấy danh sách thể loại
        url_movie = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url_movie)
        response.raise_for_status()
        data_movie = response.json()
        genres = data_movie.get('genres', [])
        countries = data_movie.get('production_countries', [])

        context['top_rated_movies'] = top_rated_movies
        context['related_movies'] = related_movies
        context.update({
            'movie_id': movie_id,
            'casts': casts,
            'first_row': first_row,
            'second_row': second_row,
            'genres': genres,
            'countries': countries,
            'directors': directors,
        })

        reviews = movie.reviews.all()
        context['reviews'] = reviews

        return context

movie_detail_view = MovieDetailView.as_view()

class MovieVideoView(generic.DetailView):
    model = Movie
    template_name = 'movies/watch_video.html'  # Tạo một template mới cho việc xem video
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_id = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=movie_id)
        url_movie = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/videos?api_key={API_KEY}&language=en-US'
        
        try:
            response = requests.get(url_movie)
            response.raise_for_status()
            data_movie = response.json()
            
            results = data_movie.get("results", [])
            
            if results:
                keys = [result.get("key") for result in results]
                context['keys'] = keys
        except requests.exceptions.RequestException as e:
            context['error'] = str(e)
            
        return context


movie_video_view = MovieVideoView.as_view()

def search_movie(request):
    context = {}
    search = request.GET.get('search','')
    if search:
        movies = Movie.objects.search(search)
        movies_per_page = 12
        paginator = Paginator(movies, movies_per_page)
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']
        else:
            page = 1
        
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)
        context['object_list'] = movies
    else:
        context['not_search'] = True
    return render(request, "movies/find.html", context)