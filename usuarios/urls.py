from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import cadastro, perfil, login

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login, name='login'),
    path('perfil/', perfil, name='perfil'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('resetar-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('resetar-senha/sucesso/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetar-senha/completo/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]