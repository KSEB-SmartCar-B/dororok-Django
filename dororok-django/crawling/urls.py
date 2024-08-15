from django.urls import path
from .views import chart_view, model_train

urlpatterns = [
    path('chart/<str:genre>/', chart_view, name='chart_view'),
    path('train/', model_train, name='model_train'),
]