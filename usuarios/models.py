from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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

@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()