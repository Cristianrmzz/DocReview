from django.urls import path
from . import views

app_name = 'dashboard'  # Namespace opcional pero recomendado

urlpatterns = [
    path('', views.index, name='index'),
    path('cargar/', views.cargar_documentos, name='cargar_documentos'),
    path('descargar/<int:documento_id>/', views.descargar_documento, name='descargar_documento'),
    path('marcar-revisado/<int:documento_id>/', views.marcar_revisado, name='marcar_revisado'),
]