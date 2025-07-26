from django.db import models
from django.conf import settings
from django.utils import timezone


class Material(models.Model):
    SLIDE = 'SL'
    VIDEO = 'VD'
    DOCUMENTO = 'DC'
    TIPO_CHOICES = [
        (SLIDE, 'Slide'),
        (VIDEO, 'Vídeo'),
        (DOCUMENTO, 'Documento'),
    ]
    
    autor = models.CharField(max_length=100)
    descricao = models.TextField(max_length=100)
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(
        max_length=2,
        choices=TIPO_CHOICES,
        default=DOCUMENTO,
    )
    arquivo = models.FileField(upload_to='meus_materiais/')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Define um valor padrão
    data_compartilhado = models.DateTimeField(null=True, default=timezone.now)

    
    def __str__(self):
        return self.titulo
    

class MaterialSalvo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    data_salvo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} salvou {self.material.titulo}"