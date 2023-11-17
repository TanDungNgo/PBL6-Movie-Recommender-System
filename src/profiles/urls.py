from django.urls import path, include
from . import views  # Thay thế bằng tên module và view của bạn

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
   
]
