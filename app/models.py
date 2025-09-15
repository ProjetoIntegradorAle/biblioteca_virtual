from django.db import models
from django.contrib.auth.models import User
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
    
    avaliacoes_habilitadas = models.BooleanField(default=False)

    colaboracao_habilitada = models.BooleanField(default=False)
    colaboradores_pendentes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="convites_recebidos",
        blank=True
    )
    colaboradores_confirmados = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="colaboracoes_confirmadas",
        blank=True
    )
    
    curtidas = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='materiais_curtidos',
        blank=True
    )

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)  # Define um valor padrão
    data_compartilhado = models.DateTimeField(null=True, default=timezone.now)

    
    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    curtidas = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comentarios_curtidos', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

class MaterialSalvo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    data_salvo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} salvou {self.material.titulo}"
    
class HistoricoPesquisa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    termo = models.CharField(max_length=255)
    url_resultado = models.URLField()
    data_pesquisa = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.termo} ({self.data_pesquisa.strftime('%d/%m/%Y %H:%M')})"