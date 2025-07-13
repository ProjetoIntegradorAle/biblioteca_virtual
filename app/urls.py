from django.urls import path
from . import views
from usuarios.views import perfil

urlpatterns = [
    path('', views.index, name="index"),
    path('meus_materiais/', views.meus_materiais, name="meus_materiais"),
    path('sobre/', views.sobre, name="sobre"),
    path('configuracoes/', views.configuracoes, name="configuracoes"),
    path('conta_conf/', views.conta_conf, name="conta_conf"),
    path('notifica_conf/', views.notifica_conf, name="notifica_conf"),
    
    path('adicionar', views.adicionar_material, name='adicionar_material'),
    path('editar/<int:id_material>/', views.editar_material, name='editar_material'),
    path('deletar/<int:id_material>/', views.deletar_material, name='deletar_material'),
    path('visualizar/<int:id_material>/', views.visualizar_material, name='visualizar_material'),
    path('perfil/', perfil, name="perfil"),
    path('buscar/', views.buscar_materiais, name='buscar_materiais'),
    path('salvar/<int:id_material>/', views.salvar_material, name='salvar_material'),
]