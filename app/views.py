from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material, MaterialSalvo, Comentario, HistoricoPesquisa
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.http import urlencode
from django.http import JsonResponse
from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

def sobre(request):
    return render(request, 'sobre.html')

@login_required
def configuracoes(request):
    return render(request, 'config-templates/configuracoes.html')

def mat_compart(request):
    usuario = request.user  # Usuário logado
    materiais = Material.objects.filter(usuario=usuario)
    return render(request, 'config-templates/mat_compart.html', {'materiais': materiais})

@login_required
def histor_pesq(request):
    historico = HistoricoPesquisa.objects.filter(usuario=request.user).order_by('-data_pesquisa')
    return render(request, 'config-templates/histor_pesq.html', {'historico': historico})

def permissoes_avali(request):
    materiais_permitidos = Material.objects.filter(avaliacoes_habilitadas=True)
    return render(request, 'config-templates/permissoes_avali.html', {
        'materiais': materiais_permitidos
    })

def convit_colabora(request):
    usuario = request.user
    materiais = Material.objects.filter(usuario=usuario)
    convites_recebidos = Material.objects.filter(colaboradores_pendentes=usuario)
    return render(request, 'config-templates/convit_colabora.html', {
        'materiais': materiais,
        'convites_recebidos': convites_recebidos
    })

def save(self, *args, **kwargs):
    if self.colaboradores_confirmados.count() > 1:
        raise ValueError("Só é permitido um colaborador por material.")
    super().save(*args, **kwargs)
    
def buscar_usuarios(request):
    termo = request.GET.get('q', '')
    resultados = User.objects.filter(username__icontains=termo)[:5]
    data = [{'id': u.id, 'nome': u.username} for u in resultados]
    return JsonResponse(data, safe=False)

################################## COMENTÁRIOS-CURTIDAS ########################################
def material_detalhe(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, 'material_detalhe.html', {'material': material})

def avaliacao_receb(request):
    materiais_com_interacoes = Material.objects.filter(autor=request.user).prefetch_related('comentarios', 'curtidas')
    return render(request, 'config-templates/avaliacao_receb.html', {'materiais': materiais_com_interacoes})

@login_required
def comentar(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        texto = request.POST.get('comentario')
        Comentario.objects.create(
            autor=request.user,
            material=material,
            texto=texto
        )
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def curtir_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    # Alternar curtida (curtir/descurtir)
    if request.user in material.curtidas.all():
        material.curtidas.remove(request.user)
    else:
        material.curtidas.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', '/'))
#################################### COMENTÁRIOS-CURTIDAS ##########################################

@login_required
def meus_materiais(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            novo_material = form.save(commit=False)
            novo_material.usuario = request.user
            novo_material.autor = request.user.username
            novo_material.save()

            # Verifica se colaboração está habilitada
            colaboracao_habilitada = request.POST.get('colaboracao_habilitada')
            colaborador_id = request.POST.get('colaborador_id')

            if colaboracao_habilitada and colaborador_id:
                try:
                    colaborador = User.objects.get(id=colaborador_id)

                    # Verifica se já há colaborador pendente
                    if novo_material.colaboradores_pendentes.count() >= 1:
                        messages.warning(request, 'Só é permitido um colaborador por material.')
                    else:
                        novo_material.colaboracao_habilitada = True
                        novo_material.colaboradores_pendentes.add(colaborador)
                        novo_material.save()
                except User.DoesNotExist:
                    messages.warning(request, 'Colaborador não encontrado.')

            messages.success(request, 'Material criado com sucesso!')
            return redirect('meus_materiais')
        else:
            messages.error(request, 'Erro ao criar material. Verifique os campos.')
    else:
        form = MaterialForm()

    materiais_criados = Material.objects.filter(usuario=request.user)
    paginator = Paginator(materiais_criados, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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

        # Salvar no histórico
        url_resultado = request.build_absolute_uri('?'+urlencode({'q': query}))
        HistoricoPesquisa.objects.create(
            usuario=request.user,
            termo=query,
            url_resultado=url_resultado
        )

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

