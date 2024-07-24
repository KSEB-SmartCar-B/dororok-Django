from django.urls import path
#from rest_framework.routers import DefaultRouter
from swagger.views import TestView, SerializerView

app_name = 'swagger'

urlpatterns = [
    path('', TestView.as_view(), name='test'),
    path('serializer/', SerializerView.as_view(), name='serializer'),
]