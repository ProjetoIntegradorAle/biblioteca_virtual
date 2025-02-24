from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return self.username
    
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    localizacao = models.CharField(max_length=30, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username