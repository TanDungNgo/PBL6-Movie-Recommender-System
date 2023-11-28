from .models import Review
from django.shortcuts import redirect
from movies.models import Movie
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

@require_http_methods(['POST'])
def add_review(request):
    if not request.htmx:
        return HttpResponse("Not Allowed", status=400)
    object_id = request.POST.get('object_id')
    content = request.POST.get('content')
    user = request.user
    message = "<span class='bg-danger text-light py-1 px-3 rounded'>You must <a href='/accounts/login'>login</a> to review this.</div>"
    if content == "" or content is None:
        message = "<span class='bg-danger text-light py-1 px-3 rounded'>You must write a review.</div>"
        return HttpResponse(message,status=200)
    if user.is_authenticated:
        message = "<span class='bg-danger text-light py-1 px-3 rounded'>An error occured.</div>"
        ctype = ContentType.objects.get(app_label='movies', model='movie')
        review_obj = Review.objects.create(content_type=ctype, object_id=object_id, content=content, user=user)
        if review_obj.content_object is not None:
            message = "<span class='bg-success text-light py-1 px-3 rounded'>Review saved!</div>"
            
    return HttpResponse(message,status=200)