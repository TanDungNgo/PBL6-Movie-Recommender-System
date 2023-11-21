from django.urls import path, include
from . import views  

urlpatterns = [
    path('login/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
]
