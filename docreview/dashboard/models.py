from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Documento(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('revisado', 'Revisado'),
    )
    
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')
    fecha_carga = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    def __str__(self):
        return self.nombre