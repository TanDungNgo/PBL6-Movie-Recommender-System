from .models import Review
from django.shortcuts import redirect
from movies.models import Movie
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from profiles.models import CustomUser
from django.shortcuts import get_object_or_404

@require_http_methods(['POST'])
def review_movie(request):
    if request.method == 'POST':
            object_id = request.POST.get('object_id', None)
            content = request.POST.get('content', None)
            user = request.user
            customUser = CustomUser.objects.get(id=user.id)

            if user.is_authenticated:
                ctype = ContentType.objects.get(app_label='movies', model='movie')
                review_obj = Review.objects.create(content_type=ctype, object_id=object_id, content=content, user=customUser)
                
                if review_obj.content_object is not None:
                    response_data = {
                        'status': 'success',
                        'message': 'Review submitted successfully!',
                        'review': {
                            'id': review_obj.id,
                            'content': review_obj.content,
                            'user': review_obj.user.first_name + ' ' + review_obj.user.last_name,
                            'avatar': review_obj.user.avatar,
                            'timestamp': review_obj.timestamp.strftime("%b. %d, %Y, %I:%M %p"),
                        },
                    }
                    return JsonResponse(response_data)
                else:
                    response_data = {
                        'status': 'error',
                        'message': 'An error occurred',
                    }
                    return JsonResponse(response_data)
            else:
                response_data = {
                    'status': 'error',
                    'message': 'You must log in to submit a review',
                }
                return JsonResponse(response_data)
    else:
        response_data = {
            'status': 'error',
            'message': 'Invalid request method',
        }
        return JsonResponse(response_data)
    

def load_more_reviews(request):
    current_count = int(request.GET.get('current_count'))
    load_count = int(request.GET.get('load_count'))
    object_id = request.GET.get('object_id')

    # Query để lấy thêm đánh giá
    movie = Movie.objects.get(id=object_id)
    reviews = movie.reviews.all()[current_count: current_count + load_count]

    # Render HTML cho các đánh giá mới
    reviews_html = render_to_string('reviews/snippet/review_list.html', {'reviews': reviews, 'request': request})

    # Kiểm tra xem đã tải hết tất cả đánh giá hay chưa
    all_loaded = len(reviews) < load_count

    return JsonResponse({
        'reviews_html': reviews_html,
        'loaded_count': len(reviews),
        'all_loaded': all_loaded,
    })

def delete_review(request):
    review_id = request.POST.get('review_id')
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return JsonResponse({'status': 'success', 'message': 'Review deleted successfully!'})

def update_review(request):
    review_id = request.POST.get('review_id')
    review = get_object_or_404(Review, id=review_id)
    review.content = request.POST.get('content')
    review.save()
    response_data = {
        'status': 'success',
        'message': 'Review updated successfully!',
        'review': {
            'id': review.id,
            'content': review.content,
            'user': review.user.first_name + ' ' + review.user.last_name,
            'avatar': review.user.avatar,
            'timestamp': review.timestamp.strftime("%b. %d, %Y, %I:%M %p"),
        },
    }
    return JsonResponse(response_data)