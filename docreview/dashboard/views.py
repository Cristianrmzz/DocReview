
from django.shortcuts import render

def index(request):
    return render(request, 'dashboard.html')

def cargar_view(request):
    return render(request, 'cargar.html')