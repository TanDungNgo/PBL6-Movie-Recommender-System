from django.shortcuts import render
from django.views import generic

from .models import Movie

# Create your views here.
class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 10
    queryset = Movie.objects.all().order_by('-rating_avg')

movie_list_view = MovieListView.as_view()

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    queryset = Movie.objects.all()

movie_detail_view = MovieDetailView.as_view()
