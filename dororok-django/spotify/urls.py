from django.urls import path
from .views import search_music_or_artist

urlpatterns = [
    path('search/', search_music_or_artist, name='search_music_or_artist')
]