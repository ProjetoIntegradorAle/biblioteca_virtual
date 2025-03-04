from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FormCadastro, FormPerfil
from .models import Perfil
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm

def cadastro(request):
    if request.method == 'POST':
        form = FormCadastro(request.POST)
        if form.is_valid():
            user = form.save()
            # Verifica se o perfil já existe antes de criar um novo
            perfil, created = Perfil.objects.get_or_create(user=user)
            if created:
                messages.success(request, 'Cadastro realizado com sucesso!')
            else:
                messages.warning(request, 'O perfil já existe.')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao realizar o cadastro!')
    else:
        form = FormCadastro()
    return render(request, 'cadastro.html', {'form': form})

def login(request): 
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')  # Redireciona para a página inicial após o logout

@login_required
def perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = FormPerfil(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Erro ao atualizar o perfil!')
    else:
        form = FormPerfil(instance=perfil)
    return render(request, 'perfil.html', {'form': form})

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Atualiza a sessão do usuário para evitar logout
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('perfil')  # Redireciona para a página de perfil
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'alterar_senha.html', {'form': form})