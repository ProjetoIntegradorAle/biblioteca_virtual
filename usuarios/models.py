from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=400, blank=True)
    cidade = models.CharField(max_length=50, null=True)
    estado = models.CharField(max_length=50, null=True)
    data_nascimento = models.DateField(null=True)
    telefone = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username
