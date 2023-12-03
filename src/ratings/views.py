from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import Rating

@require_http_methods(['POST'])
def rate_movie(request):
    if not request.htmx:
        return HttpResponse("Not Allowed", status=400)
    object_id = request.POST.get('object_id')
    rating_value = request.POST.get("rating_value")
    if object_id is None or rating_value is None:
        return HttpResponse("Skipping", status = 200)
    user = request.user
    message = "<span class='bg-danger text-light py-1 px-3 rounded'>You must <a href='/accounts/login'>login</a> to rate this.</div>"
    if user.is_authenticated:
        message = "<span class='bg-danger text-light py-1 px-3 rounded'>An error occured.</div>"
        # messages.error(request, 'An error occured.')
        ctype = ContentType.objects.get(app_label='movies', model='movie')
        rating_obj = Rating.objects.create(content_type=ctype, object_id=object_id, value=rating_value, user=user)
        if rating_obj.content_object is not None:
            message = "<span class='bg-success text-light py-1 px-3 rounded'>Rating saved!</div>"
            # messages.success(request, 'Rating saved!')
    return HttpResponse(message,messages,status=200)