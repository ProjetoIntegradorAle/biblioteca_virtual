from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import FormCadastro, FormPerfil, FormRecuperaSenha, FormRedefineSenha
from .models import Perfil

def cadastro(request):
    if request.method == 'POST':
        form = FormCadastro(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(user=user)
            return redirect('login')
    else:
        form = FormCadastro()
    return render(request, 'cadastro.html', {'form': form})

@login_required
def perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = FormPerfil(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FormPerfil(instance=perfil)
    return render(request, 'perfil.html', {'form': form})

class RecuperaSenhaView(PasswordResetView):
    form_class = FormRecuperaSenha
    template_name = 'recupera_senha.html'

class RedefineSenhaView(PasswordResetConfirmView):
    form_class = FormRedefineSenha
    template_name = 'confirma_senha.html'