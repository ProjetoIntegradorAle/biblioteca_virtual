from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import cadastro, perfil, login, editar_perfil

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login, name='login'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('alterar-senha/sucesso/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('resetar-senha/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('resetar-senha/sucesso/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('resetar-senha/confirmar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('resetar-senha/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    path('editar-perfil/', editar_perfil, name='editar_perfil'),  # Nova rota para editar perfil
]