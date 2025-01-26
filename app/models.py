from django.db import models

class Material(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    autor = models.CharField(max_length=60)
    tipo = models.CharField(max_length=30)