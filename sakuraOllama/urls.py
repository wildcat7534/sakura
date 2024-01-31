from django.urls import path
from . import views

app_name = 'sakuraOllama'

urlpatterns = [
  path('', views.sakura, name='sakura'),
  path('sakuravllm', views.sakuraVllm, name='sakuravllm'),
  path('sakuraTransormers', views.sakuraTransormers, name='sakuraTransormers'),
]
