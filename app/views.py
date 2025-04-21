from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material
from .forms import MaterialForm
from django.core.paginator import Paginator

def index(request):
    return render(request, 'index.html')

@login_required
def meus_materiais(request):
    form = MaterialForm()
    materiais = Material.objects.filter(usuario=request.user)  # Filtra materiais pelo usuário logado
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
            material = form.save(commit=False)
            material.usuario = request.user  # Usuário logado como o autor do material
            material.autor = request.user.username  # Nome do usuário como autor
            material.save()
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

@login_required
def buscar_materiais(request):
    query = request.GET.get('q')  # Captura o termo de busca do input do usuário.
    materiais = Material.objects.all()  # Busca todos os materiais inicialmente.

    if query:
        materiais = materiais.filter(
            titulo__icontains=query,  # Filtra materiais cujo título contém o termo de busca.
            autor__icontains=query,
            descricao__icontains=query,
            tipo__icontains=query
        )

    return render(request, 'busca.html', {'materiais': materiais})