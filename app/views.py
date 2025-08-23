from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material, MaterialSalvo, Comentario
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

def configuracoes(request):
    return render(request, 'configuracoes.html')

def mat_compart(request):
    usuario = request.user  # Usuário logado
    materiais = Material.objects.filter(usuario=usuario)
    return render(request, 'mat_compart.html', {'materiais': materiais})

################################## COMENTÁRIOS-CURTIDAS ########################################
def material_detalhe(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, 'material_detalhe.html', {'material': material})

def coment_receb(request):
    # Implementar lógica para exibir comentários recebidos
    return render(request, 'coment_receb.html')

def comentar(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        Comentario.objects.create(
            autor=request.user,
            material=material,
            texto=texto
        )
    return redirect('material_detalhe', material_id=material.id)

def curtir_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    # Alternar curtida (curtir/descurtir)
    if request.user in material.curtidas.all():
        material.curtidas.remove(request.user)
    else:
        material.curtidas.add(request.user)

    return redirect('material_detalhe', material_id=material.id)
#################################### COMENTÁRIOS-CURTIDAS ##########################################


def histor_pesq(request):
    # Implementar lógica para exibir histórico de pesquisa
    return render(request, 'histor_pesq.html')

def permis_coment(request):
    # Implementar lógica para gerenciar permissões de comentários
    return render(request, 'permis_coment.html')

def convit_colabora(request):
    # Implementar lógica para gerenciar convites de colaboração
    return render(request, 'convit_colabora.html')

@login_required
def meus_materiais(request):
    # Se for POST, trata a criação de novo material
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            novo_material = form.save(commit=False)
            novo_material.usuario = request.user
            novo_material.autor = request.user.username
            novo_material.save()
            messages.success(request, 'Material criado com sucesso!')
            return redirect('meus_materiais')  # Evita reenvio do formulário
        else:
            messages.error(request, 'Erro ao criar material. Verifique os campos.')
    else:
        form = MaterialForm()

    # Materiais criados pelo usuário logado
    materiais_criados = Material.objects.filter(usuario=request.user)

    # Paginação dos materiais criados
    paginator = Paginator(materiais_criados, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Materiais salvos pelo usuário, separados por tipo
    documentos_salvos = MaterialSalvo.objects.filter(usuario=request.user, material__tipo='Documento')
    videos_salvos = MaterialSalvo.objects.filter(usuario=request.user, material__tipo='Vídeo')
    slides_salvos = MaterialSalvo.objects.filter(usuario=request.user, material__tipo='Slide')

    return render(request, 'meus_materiais.html', {
        'form': form,
        'page_obj': page_obj,
        'documentos_salvos': documentos_salvos,
        'videos_salvos': videos_salvos,
        'slides_salvos': slides_salvos,
    })

@login_required
def visualizar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material)
    return render(request, 'visualizar_material.html', {'material': material})

@login_required
def editar_material(request, id_material):
    material = get_object_or_404(Material, pk=id_material, usuario=request.user)

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

    # Renderiza o mesmo template usado em meus_materiais
    return render(request, 'meus_materiais.html', {
        'form': form,
        'editando': True,  # Flag opcional para mostrar que está em modo de edição
    })

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