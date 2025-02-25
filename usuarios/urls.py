from django.urls import path
from django.contrib.auth import views as auth_views
from .views import cadastro, perfil, RecuperaSenhaView, RedefineSenhaView

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('perfil/', perfil, name='perfil'),
    path('recupera_senha/', RecuperaSenhaView.as_view(), name='recupera_senha'),
    path('confirma_senha/<uidb64>/<token>/', RedefineSenhaView.as_view(), name='confirma_senha'),
    path('senha_enviada/', auth_views.PasswordResetDoneView.as_view(template_name='senha_enviada.html'), name='senha_enviada'),
    path('senha_redefinida/', auth_views.PasswordResetCompleteView.as_view(template_name='senha_redefinida.html'), name='senha_redefinida'),
]
