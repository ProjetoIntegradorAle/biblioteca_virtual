from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material
from .forms import MaterialForm
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

def login(request): 
    return render(request, 'registration/login.html')

def meus_materiais(request):
    form = MaterialForm()
    materiais = Material.objects.all()
    paginator = Paginator(materiais, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'meus_materiais.html', {
        'form': form,
        'page_obj': page_obj,
    })

@login_required
def adicionar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material adicionado com sucesso!')
            return redirect('meus_materiais')
        else:
            messages.error(request, 'Erro ao adicionar material!')
    else:
        form = MaterialForm()
    return render(request, 'adicionar_material.html', {'form': form})


@login_required
def visualizar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    return render(request, 'visualizar_material.html', {'material': material})

@login_required
def editar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material atualizado com sucesso!')
            return redirect('meus_materiais')
        else:
            messages.error(request, 'Erro ao atualizar material!')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'adicionar_material.html', {'form': form})

@login_required
def deletar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material deletado com sucesso!')
        return redirect('meus_materiais')
    return render(request, 'deletar_material.html', {'material': material})

