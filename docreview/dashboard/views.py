from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Documento
from .forms import DocumentUploadForm
from django.http import FileResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from .decorators import superuser_required


@login_required
def index(request):
    # Obtener estadísticas
    total_documentos = Documento.objects.count()
    documentos_revisados = Documento.objects.filter(estado='revisado').count()
    documentos_pendientes = Documento.objects.filter(estado='pendiente').count()
    total_usuarios = User.objects.count() if 'auth.User' in str(User) else 0
    
    # Obtener documentos recientes
    documentos_recientes = Documento.objects.all().order_by('-fecha_carga')[:10]
    # Documentos específicos según el usuario
    if request.user.is_superuser:
        # Superusuarios ven todos los documentos
        documentos_recientes = Documento.objects.all().order_by('-fecha_carga')[:10]
        documentos_revisados = Documento.objects.filter(estado='revisado').count()
        documentos_pendientes = Documento.objects.filter(estado='pendiente').count()
        total_usuarios = User.objects.count() if 'auth.User' in str(User) else 0
    else:
        # Usuarios normales solo ven sus propios documentos
        documentos_recientes = Documento.objects.filter(usuario=request.user).order_by('-fecha_carga')[:10]
        documentos_revisados = Documento.objects.filter(usuario=request.user, estado='revisado').count()
        documentos_pendientes = Documento.objects.filter(usuario=request.user, estado='pendiente').count()
        total_usuarios = 0  # No necesitan ver esto
    context = {
        'total_documentos': total_documentos,
        'documentos_revisados': documentos_revisados,
        'documentos_pendientes': documentos_pendientes,
        'total_usuarios': total_usuarios,
        'documentos_recientes': documentos_recientes
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def cargar_documentos(request):
    mensaje = None
    archivos_cargados = []
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            documentos = request.FILES.getlist('documents')
            for doc in documentos:
                # Crear una instancia del modelo Documento
                documento = Documento(
                    nombre=doc.name,
                    archivo=doc,
                    usuario=request.user if request.user.is_authenticated else None
                )
                documento.save()
                archivos_cargados.append(doc.name)
            
            mensaje = "Documentos cargados correctamente"
    else:
        form = DocumentUploadForm()
    
    context = {
        'form': form,
        'mensaje': mensaje,
        'archivos_cargados': archivos_cargados
    }
    return render(request, 'cargar.html', context)

@login_required
@superuser_required
def descargar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    return FileResponse(documento.archivo, as_attachment=True, filename=documento.nombre)

@login_required
@superuser_required
def marcar_revisado(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    documento.estado = 'revisado'
    documento.save()
    messages.success(request, f"Documento '{documento.nombre}' marcado como revisado")
    return redirect('dashboard:index')

@login_required
def redirect_to_dashboard(request):
    return redirect('dashboard:index')

@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:index')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


@login_required
@superuser_required
def eliminar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    nombre_documento = documento.nombre
    documento.delete()
    messages.success(request, f"Documento '{nombre_documento}' eliminado correctamente")
    return redirect('dashboard:index')

def inicio(request):
    return render(request, 'inicio.html')