from django.shortcuts import render
from django.views import generic
from django.db.models import Avg

from .models import Movie

# Create your views here.
class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 10
    # context -> object_list
    queryset = Movie.objects.all().order_by('-rating_avg')

movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        top_rated_movies = Movie.objects.all().order_by('-rating_avg')[:10]
        
        context['top_rated_movies'] = top_rated_movies
        return context

movie_detail_view = MovieDetailView.as_view()
