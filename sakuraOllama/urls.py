from django.urls import path
from . import views

app_name = 'sakuraOllama'

urlpatterns = [
  path('', views.sakuraAsync, name='sakuraasync'),
"""   path('sakuravllm', views.sakuraVllm, name='sakuravllm'),
  path('sakuraTransormers', views.sakuraTransormers, name='sakuraTransormers'),
  path('sakuraasync', views.sakuraAsync, name='sakuraasync'), """
]
