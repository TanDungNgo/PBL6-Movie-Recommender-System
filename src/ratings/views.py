from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from .models import Rating
User = get_user_model()
# Create your views here.

@require_http_methods(['POST'])
def rate_movie_view(request):
    if not request.htmx:
        return HttpResponse("Not Allowed", status = 400)
    object_id = request.POST.get('object_id')
    rating_value = request.POST.get("rating_value")
    user = request.user
    message = "You must <a href = '/accounts/login'>login</a> to rate this"
    if user.is_authenticated:
        message = "<span class = 'bg-danger text-light py-1 px-3 rounded'> An error occured.</div>"
        ctype = ContentType.objects.get(app_lable = 'movies', model='movie')
        rating_obj = Rating.objects.create(content_type = ctype, object_id= object_id, value= rating_value, user=user)
        if rating_obj.content_object is not None:
            message = "<span class = 'bg-success text-light py-1 px-3 rounded'> Success!</div>"

    return HttpResponse(message, status = 200)

