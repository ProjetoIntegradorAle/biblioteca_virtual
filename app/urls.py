from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('meus_materiais/', views.meus_materiais, name="meus_materiais"),
    path('login/', views.login, name='login'),
]

