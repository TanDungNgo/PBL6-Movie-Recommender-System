from movies.models import Movie


def movies_list(request):
    movies_list = list(Movie.objects.values_list('title', flat=True))
    return {'movies_list': movies_list}