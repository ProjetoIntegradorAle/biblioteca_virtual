from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import FormCadastro, FormPerfil, FormRecuperaSenha, FormRedefineSenha
from .models import Perfil
from django.contrib import messages

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

class RecuperaSenhaView(PasswordResetView):
    form_class = FormRecuperaSenha
    template_name = 'recupera_senha.html'

class RedefineSenhaView(PasswordResetConfirmView):
    form_class = FormRedefineSenha
    template_name = 'confirma_senha.html'