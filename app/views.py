from django.shortcuts import render, redirect
from .forms import MaterialForm
from .models import Material

def index(request):
    return render(request, 'index.html')

def adicionar_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('meus_materiais')
    else:
        form = MaterialForm()
    return render(request, 'adicionar_material.html', {'form': form})

def meus_materiais(request):
    videos = Material.objects.filter(tipo=Material.VIDEO)
    slides = Material.objects.filter(tipo=Material.SLIDE)
    documentos = Material.objects.filter(tipo=Material.DOCUMENTO)
    return render(request, 'meus_materiais.html', {
        'videos': videos,
        'slides': slides,
        'documentos': documentos,
    })
