from django.shortcuts import render
from django.views import generic
from movies.models import Movie

# Create your views here.
class DashboardView(generic.TemplateView):
    template_name = 'admin_page/dashboard.html'

dashboard_view = DashboardView.as_view()

class MovieListView(generic.ListView):
    model = Movie
    template_name = 'admin_page/movie_list.html'
    context_object_name = 'movies'

movie_list_view = MovieListView.as_view()

class UserListView(generic.TemplateView):
    template_name = 'admin_page/user_list.html'

user_list_view = UserListView.as_view()

class MovieCreateView(generic.TemplateView):
    template_name = 'admin_page/movie_create.html'

movie_create_view = MovieCreateView.as_view()