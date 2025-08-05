from django.urls import path
from . import views
from usuarios.views import perfil

urlpatterns = [
    path('', views.index, name="index"),
    path('meus_materiais/', views.meus_materiais, name="meus_materiais"),
    path('sobre/', views.sobre, name="sobre"),
    
    path('adicionar', views.adicionar_material, name='adicionar_material'),
    path('editar/<int:id_material>/', views.editar_material, name='editar_material'),
    path('deletar/<int:id_material>/', views.deletar_material, name='deletar_material'),
    path('visualizar/<int:id_material>/', views.visualizar_material, name='visualizar_material'),
    path('perfil/', perfil, name="perfil"),
    path('buscar/', views.buscar_materiais, name='buscar_materiais'),
    path('salvar/<int:id_material>/', views.salvar_material, name='salvar_material'),
    
    path('configuracoes/', views.configuracoes, name="configuracoes"),
    path('mat_compart/', views.mat_compart, name="mat_compart"),
    path('coment_receb/', views.coment_receb, name="coment_receb"),
    path('histor_pesq/', views.histor_pesq, name="histor_pesq"),
    path('permis_coment/', views.permis_coment, name="permis_coment"),
    path('convit_colabora/', views.convit_colabora, name="convit_colabora"),
    path('material/<int:material_id>/', views.material_detalhe, name='material_detalhe'),
    path('material/<int:material_id>/comentar/', views.comentar, name='comentar'),
    path('curtir_material/<int:material_id>/', views.curtir_material, name='curtir_material'),
]