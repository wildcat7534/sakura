from django.urls import path
from . import views

app_name = 'sakuraOllama'

urlpatterns = [
  path('', views.sakuraAsync, name='sakuraasync'),
]
