from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material, MaterialSalvo
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def configuracoes(request):
    return render(request, 'configuracoes.html')

def conta_conf(request):
    return render(request, 'conta_conf.html')

def notifica_conf(request):
    return render(request, 'notifica_conf.html')

@login_required
def meus_materiais(request):
    form = MaterialForm() 
    materiais_criados = Material.objects.filter(usuario=request.user) # Materiais criados pelo usuário logado
    # Materiais salvos pelo usuário logado, separados por tipo
    documentos_salvos = MaterialSalvo.objects.filter(usuario=request.user, material__tipo='Documento')
    videos_salvos = MaterialSalvo.objects.filter(usuario=request.user, material__tipo='Vídeo')
    slides_salvos = MaterialSalvo.objects.filter(usuario=request.user, material__tipo='Slide')

    # Paginação para materiais criados
    paginator = Paginator(materiais_criados, 6)
    page_number = request.GET.get('page')  # Número da página
    page_obj = paginator.get_page(page_number)

    return render(request, 'meus_materiais.html', {
        'form': form,
        'page_obj': page_obj,  # Materiais criados paginados
        'documentos_salvos': documentos_salvos,
        'videos_salvos': videos_salvos,
        'slides_salvos': slides_salvos,
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
    query = request.GET.get('q')
    materiais = Material.objects.none()  

    if query:
        materiais = Material.objects.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(descricao__icontains=query) |
            Q(tipo__icontains=query)
        )

    print("Materiais encontrados:", materiais)  # Verifique se a consulta retorna objetos

    return render(request, 'busca.html', {'materiais': materiais})

@login_required
def salvar_material(request, id_material):
    if request.method == 'POST':
        material = get_object_or_404(Material, id=id_material)  # Verifica se o material existe
        material_existente = MaterialSalvo.objects.filter(usuario=request.user, material=material).exists()
        if not material_existente:
            MaterialSalvo.objects.create(usuario=request.user, material=material)  # Cria o vínculo no banco
            print(f"Material salvo: {material.titulo}")  # Exibe confirmação no console
        else:
            print(f"O material já está salvo: {material.titulo}")
        
        return redirect('meus_materiais')