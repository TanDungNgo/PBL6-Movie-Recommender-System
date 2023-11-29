import datetime
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from django.db.models import Exists, OuterRef
from ratings.models import Rating
from .models import CustomUser

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


from faker import Faker
def ConvertUserToCustomUser():
    users = User.objects.all()
    fake = Faker() 
    for user in users:
        profile = fake.profile()
        gender = profile.get("sex")
        if gender == 'Male' or gender == 'male' or gender == 'M':
            avatar = "https://cdn-icons-png.flaticon.com/512/4998/4998641.png"
        else:
            avatar = "https://cdn-icons-png.flaticon.com/512/4999/4999076.png"
        custom_user = CustomUser(
        id = user.id,
        username=user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        email=user.email,
        password=user.password, 
        is_active=user.is_active,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
        last_login=user.last_login,
        date_joined=user.date_joined,
        gender = gender,
        avatar = avatar,
        address = profile.get("address"))
        custom_user.save()
        print(custom_user)