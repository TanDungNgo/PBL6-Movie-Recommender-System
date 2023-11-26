from django.shortcuts import render, redirect

from movies.models import Movie
from suggestions.models import Suggestion

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
        context['object_list'] = qs[:max_movies]
    else:
        context['object_list'] = Movie.objects.all().order_by("?")[:max_movies]
    return render(request, "movies/suggestion.html", context)