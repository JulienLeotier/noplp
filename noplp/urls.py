"""noplp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start),
    path('challenge', views.challenge),
    path('photobooth', views.photobooth),
    path('savePhotobooth', views.savePhotoBooth),
    path('getPhotobooth', views.getPhotobooth),
    path('getAllChallenge', views.getAllChallenge),
    path('getMyChallenge/<int:id>', views.getMyChallenge),
    path('challenge/<str:name>', views.getChallenge),
    path('challenge/<int:challengeId>/<int:groupId>/', views.postChallenge),
    path('challenge/<int:id>/',
         views.postChallengeDone),
    path('challengeDelete/<int:id>/',
         views.deleteChallengeDone),
    path('view', views.view),
    path('photos', views.hubPhoto),
    path('stream', views.stream),
    path('embed.html', views.embed),
    path('players', views.choice_player),
    path('choice_music/<int:catId>/', views.choice_music),
    path('use_music/<int:musicId>/', views.use_music),
    path('choice_cat/<int:nombre1>/<int:nombre2>/', views.choice_cat),
    path('player/<int:id>/', views.player),
    path('add_score/<int:id>/<int:nombre1>/<int:nombre2>/<int:catId>/',
         views.add_score, name='add_score'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
