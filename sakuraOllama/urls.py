from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('identification/', views.identification, name='identification'),
  # Add more paths here
]
