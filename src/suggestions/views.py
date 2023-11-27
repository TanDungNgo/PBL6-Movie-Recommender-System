from django.shortcuts import render, redirect

from movies.models import Movie
from suggestions.models import Suggestion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def suggestion_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("/accounts/login/")
    context['endless_path'] = '/'
    suggestion_qs = Suggestion.objects.filter(user=user, did_rate=False)
    max_movies = 50
    request.session['total-new-suggestions'] = suggestion_qs.count()
    if suggestion_qs.exists():
        movie_ids = suggestion_qs.order_by("-value").values_list('object_id', flat=True)
        qs = Movie.objects.by_id_order(movie_ids)
        movies  = qs[:max_movies]
    else:
        movies = Movie.objects.all().order_by("?")[:max_movies]
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
    return render(request, "movies/suggestion.html", context)