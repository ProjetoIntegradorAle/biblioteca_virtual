from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MaterialForm
from .models import Material

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'registration/login.html')

@login_required
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
    
def deletar_material(request, material_id):
    context = {
        "material": get_object_or_404(Material, pk=material_id)
    }
    