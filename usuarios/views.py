from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from .forms import CadastroForm, PerfilForm, FormRecuperaSenha, FormRedefineSenha
from .models import Perfil

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user.perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user.perfil)
    return render(request, 'perfil.html', {'form': form})

class RecuperaSenhaView(PasswordResetView):
    form_class = FormRecuperaSenha
    template_name = 'recupera_senha.html'

class RedefineSenhaView(PasswordResetConfirmView):
    form_class = FormRedefineSenha
    template_name = 'confirma_senha.html'