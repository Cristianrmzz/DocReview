
from django.shortcuts import render
from .forms import DocumentUploadForm
from django.shortcuts import redirect

def index(request):
    return render(request, 'dashboard.html')
def cargar_documentos(request):
    mensaje = None
    archivos_cargados = []
    
    form = DocumentUploadForm()
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('documents')
            
            # Crear directorio para guardar archivos si no existe
            import os
            from django.conf import settings
            
            # Definimos la ruta donde se guardarán los archivos
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            
            # Creamos el directorio si no existe
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            for file in files:
                # Generamos una ruta completa para guardar el archivo
                file_path = os.path.join(upload_dir, file.name)
                
                # Guardamos el archivo físicamente en el servidor
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                # Opcional: guardar la información del archivo en la base de datos
                # nuevo_documento = Documento(nombre=file.name, ruta=file_path)
                # nuevo_documento.save()
                
                # Guardamos el nombre del archivo para mostrarlo en la vista
                archivos_cargados.append(file.name)
            
            mensaje = "Archivos cargados correctamente"
    
    context = {
        'form': form,
        'mensaje': mensaje,
        'archivos_cargados': archivos_cargados
    }
    return render(request, 'cargar.html', context)

def redirect_to_dashboard(request):
    return redirect('dashboard:index')