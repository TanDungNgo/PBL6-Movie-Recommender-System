from django.urls import path, include
from . import views  

urlpatterns = [
    path('login/', views.signin, name='signin'),
    path('register/', views.signup, name='signup'),
    path('logout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
]
