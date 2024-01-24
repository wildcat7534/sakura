from django.urls import path
from . import views

app_name = 'sakuraOllama'

urlpatterns = [
  path('sakura', views.sakura, name='sakura'),
  # Add more paths here
]
