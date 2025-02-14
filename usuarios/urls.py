from django.urls import path
from . import views

urlpatterns = [
    path('accounts/cadastro/', views.cadastro, name='cadastro'),
]
