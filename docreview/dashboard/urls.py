from django.urls import path
from . import views

app_name = 'dashboard'  # Namespace opcional pero recomendado

urlpatterns = [
    path('', views.index, name='index'),
      # Página principal del dashboard
]