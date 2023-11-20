from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .models import Rating

User = get_user_model()

@require_POST
def rate_movie_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "You must log in to rate this movie."}, status=403)

    object_id = request.POST.get('object_id')
    rating_value = request.POST.get("rating_value")

    ctype = ContentType.objects.get(app_label='movies', model='movie')
    rating_obj, created = Rating.objects.get_or_create(
        content_type=ctype, 
        object_id=object_id, 
        user=request.user,
        defaults={'value': rating_value}
    )

    if created or rating_obj.value != rating_value:
        rating_obj.value = rating_value
        rating_obj.save()
        message = "Rating saved!"
    else:
        message = "Rating updated!"

    return JsonResponse({"success": True, "message": message})
