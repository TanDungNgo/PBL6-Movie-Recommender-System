from django.http import JsonResponse
from .models import Bookmark
from movies.models import Movie
from profiles.models import CustomUser
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@require_http_methods(['POST'])
def toggle_bookmark(request):
    movie_id = request.POST.get('movie_id')
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    customUser = CustomUser.objects.get(id=user.id)
    message = ''
    try:
        bookmark = Bookmark.objects.get(user=customUser, movie=movie)
        bookmark.delete()
        is_bookmarked = False
        message = 'Bookmark removed successfully!'
    except Bookmark.DoesNotExist:
        Bookmark.objects.create(user=customUser, movie=movie)
        is_bookmarked = True
        message = 'Bookmark added successfully!'

    response_data = {
        'status': 'success',
        'is_bookmarked': is_bookmarked,
        'message': message,
    }
    return JsonResponse(response_data)

def bookmarked_movies(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("/accounts/login/")
    context['endless_path'] = '/'
    customUser = CustomUser.objects.get(id=user.id)
    bookmark_qs = Bookmark.objects.filter(user=customUser)
    max_movies = 50
    request.session['total-new-suggestions'] = bookmark_qs.count()
    if bookmark_qs.exists():
        movie_ids = bookmark_qs.values_list('movie', flat=True)
        qs = Movie.objects.by_id_order(movie_ids)
        movies  = qs[:max_movies]
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
        movies = None
    return render(request, "movies/bookmark.html", context)