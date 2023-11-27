import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from django.db.models import Exists, OuterRef
from ratings.models import Rating

User = get_user_model()


def get_recent_users(days_ago=7, ids_only=True):
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now()  - delta
    qs = User.objects.filter(
        Q(date_joined__gte=time_delta) |
        Q(last_login__gte=time_delta) 
    )
    if ids_only:
        return qs.values_list('id', flat=True)
    return delta

def get_recent_users_ratings(days_ago=7, ids_only=True):
    delta = datetime.timedelta(days=days_ago)
    time_delta = timezone.now() - delta

    # Lấy danh sách người dùng trong khoảng thời gian
    recent_users = User.objects.filter(
        Q(date_joined__gte=time_delta) |
        Q(last_login__gte=time_delta)
    )
    # Kiểm tra xem mỗi người dùng đã có rating chưa
    users_with_ratings = recent_users.annotate(
        has_rating=Exists(
            Rating.objects.filter(user=OuterRef('pk'))
        )
    ).filter(has_rating=True)

    if ids_only:
        return users_with_ratings.values_list('id', flat=True)
    return users_with_ratings