from django.urls import path
from .views import search_track
#from rest_framework.routers import DefaultRouter

app_name = 'spotify'

urlpatterns = [
    path('search/', search_track, name='search'),
]