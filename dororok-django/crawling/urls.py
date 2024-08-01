from django.urls import path
from .views import chart_view

urlpatterns = [
    path('chart/<str:genre>/', chart_view, name='chart_view'),
]