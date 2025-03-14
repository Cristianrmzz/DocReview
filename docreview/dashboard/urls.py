from django.urls import path
from . import views

app_name = 'dashboard'  # Namespace opcional pero recomendado

urlpatterns = [
    path('', views.index, name='index'),
    path('cargar/', views.cargar_view, name='cargar'),
    # Página principal del dashboard
]