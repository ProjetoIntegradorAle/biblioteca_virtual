from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Material
from .forms import MaterialForm

def index(request):
    return render(request, 'index.html')

def login(request):  # Renomeado para login_view
    return render(request, 'registration/login.html')

@login_required
def adicionar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meus_materiais')
    else:
        form = MaterialForm()
    return render(request, 'adicionar_material.html', {'form': form})

def meus_materiais(request):
    form = MaterialForm()
    videos = Material.objects.filter(tipo=Material.VIDEO)
    slides = Material.objects.filter(tipo=Material.SLIDE)
    documentos = Material.objects.filter(tipo=Material.DOCUMENTO)
    return render(request, 'meus_materiais.html', {
        'form': form,
        'videos': videos,
        'slides': slides,
        'documentos': documentos,
    })

@login_required
def editar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('meus_materiais')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'adicionar_material.html', {'form': form})

@login_required
def deletar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    if request.method == 'POST':
        material.delete()
        return redirect('meus_materiais')
    return render(request, 'deletar_material.html')
