from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from movies.models import Movie

# Create your views here.
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'

    def test_func(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser

dashboard_view = DashboardView.as_view()

class MovieListView(generic.ListView):
    model = Movie
    template_name = 'dashboard/movie_list.html'
    context_object_name = 'movies'

movie_list_view = MovieListView.as_view()

class UserListView(generic.TemplateView):
    template_name = 'dashboard/user_list.html'

user_list_view = UserListView.as_view()

class MovieCreateView(generic.TemplateView):
    template_name = 'dashboard/movie_create.html'

movie_create_view = MovieCreateView.as_view()