from django.urls import path
from .views.music_views import get_user_music_info
from .views.place_views import get_user_place_info

urlpatterns = [
    path('music/', get_user_music_info, name='music_recommendation'),
    path('place/', get_user_place_info, name='place_recommendation'),
]