from django.urls import path
from spotify.app.search_for_track_id import search_all_genres
#from spotify.views.views import search_track
#from rest_framework.routers import DefaultRouter
from spotify.app.search_for_item import search_item


app_name = 'spotify'

urlpatterns = [
    path('search/', search_item, name='search_item'),
]