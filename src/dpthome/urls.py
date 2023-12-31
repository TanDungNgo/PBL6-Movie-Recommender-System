"""
URL configuration for dpthome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ratings import views as ratings_views
from reviews import views as reviews_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('profiles.urls')),
    path('', include('movies.urls')),
    path('', include('dptpage.urls')),
    path('rate/movie/', ratings_views.rate_movie, name='rate_movie'),
    path('dashboard/', include('dashboard.urls')),
    path('suggestions/', include('suggestions.urls')),
    path('', include('reviews.urls')),
    path('bookmark/', include('bookmarks.urls')),
]