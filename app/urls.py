from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('meus_materiais/', views.meus_materiais, name="meus_materiais"),
    path('adicionar', views.adicionar_material, name='adicionar_material'),
    path('login/', views.login, name='login'),
    path('editar/<int:id_material>/', views.editar_material, name='editar_material'),
    path('deletar/<int:id_material>/', views.deletar_material, name='deletar_material'),
    path('visualizar/<int:id_material>/', views.visualizar_material, name='visualizar_material'),
]

