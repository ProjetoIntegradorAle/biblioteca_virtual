from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material, MaterialSalvo, Comentario, HistoricoPesquisa, ConviteColaboracao
from .forms import MaterialForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.http import urlencode
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def sobre(request):
    return render(request, 'sobre.html')

@login_required
def configuracoes(request):
    return render(request, 'config-templates/configuracoes.html')

@login_required
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

def save(self, *args, **kwargs):
    if self.colaboradores_confirmados.count() > 1:
        raise ValueError("Só é permitido um colaborador por material.")
    super().save(*args, **kwargs)
    
def buscar_usuarios(request):
    termo = request.GET.get('q', '')
    resultados = User.objects.filter(username__icontains=termo)[:5]
    data = [{'id': u.id, 'nome': u.username} for u in resultados]
    return JsonResponse(data, safe=False)


## COMENTÁRIOS-CURTIDAS ##
@login_required
def material_detalhe(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, 'material_detalhe.html', {'material': material})

@login_required
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
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## 

@login_required
def meus_materiais(request):
    # Materiais salvos
    salvos = MaterialSalvo.objects.filter(usuario=request.user)
    documentos_salvos = salvos.filter(material__tipo=Material.DOCUMENTO)
    slides_salvos = salvos.filter(material__tipo=Material.SLIDE)
    videos_salvos = salvos.filter(material__tipo=Material.VIDEO)

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            novo_material = form.save(commit=False)
            novo_material.usuario = request.user
            novo_material.autor = request.user.username
            novo_material.status = 'rascunho'
            novo_material.save()

            # Verifica colaboração
            colaboracao_habilitada = request.POST.get('colaboracao_habilitada')
            email_colaborador = request.POST.get('email_colaborador')

            if email_colaborador == request.user.email:
                messages.error(request, "Você não pode se convidar para colaborar consigo mesma.")
                return redirect('meus_materiais')

            if colaboracao_habilitada and email_colaborador:
                try:
                    colaborador = User.objects.get(email=email_colaborador)

                    if novo_material.colaboradores_pendentes.count() >= 1:
                        messages.warning(request, 'Só é permitido um colaborador por material.')
                    else:
                        novo_material.colaboracao_habilitada = True
                        novo_material.status = 'aguardando'
                        novo_material.save()

                        ConviteColaboracao.objects.create(
                            material=novo_material,
                            remetente=request.user,
                            destinatario=colaborador,
                            status='pendente'
                        )
                        novo_material.colaboradores_pendentes.add(colaborador)
                except User.DoesNotExist:
                    messages.warning(request, 'Colaborador não encontrado.')
            else:
                novo_material.status = 'publicado'
                novo_material.save()

            messages.success(request, 'Material criado com sucesso!')
            return redirect('meus_materiais')
        else:
            messages.error(request, 'Erro ao criar material. Verifique os campos.')
    else:
        form = MaterialForm()

    # Apenas materiais publicados
    materiais_criados = Material.objects.filter(
        Q(usuario=request.user) | Q(colaboradores_confirmados=request.user),
        status='publicado'
    ).distinct()

    paginator = Paginator(materiais_criados, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'page_obj': page_obj,
        'documentos_salvos': documentos_salvos,
        'slides_salvos': slides_salvos,
        'videos_salvos': videos_salvos,
    }
    return render(request, 'meus_materiais.html', context)


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
    return render(request, 'busca.html', {'materiais': materiais, 'query': query})

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

################### Views's para gerenciamento de convites de colaboração ########################
@login_required
def enviar_convite(request, id_material):
    material = get_object_or_404(Material, id_material)
    if request.method == 'POST':
        email = request.POST.get('email_colaborador')
        try:
            colaborador = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")
            return redirect('material_detalhe', material_id=material.id)

        convite = ConviteColaboracao.objects.create(
            material=material,
            remetente=request.user,
            colaborador=colaborador
        )
        material.colaboradores_pendentes.add(colaborador)
        material.colaboracao_habilitada = True
        material.save()
        messages.success(request, "Convite enviado com sucesso.")
        return redirect('convites')

@login_required
def responder_convite(request, convite_id):
    convite = get_object_or_404(ConviteColaboracao, id=convite_id)
    if request.method == 'POST':
        resposta = request.POST.get('resposta')
        convite.status = resposta
        convite.data_resposta = timezone.now()
        convite.save()

        material = convite.material
        if resposta == 'aceito':
            material.colaboradores_confirmados.add(request.user)
            material.colaboradores_pendentes.remove(request.user)
        elif resposta == 'negado':
            material.colaboradores_pendentes.remove(request.user)
        material.save()
        messages.success(request, f"Convite {resposta} com sucesso.")
        return redirect('convites')
    
@login_required
def convites(request):
    recebidos = ConviteColaboracao.objects.filter(destinatario=request.user)
    enviados = ConviteColaboracao.objects.filter(remetente=request.user)
    return render(request, 'config-templates/convites.html', {
        'recebidos': recebidos,
        'enviados': enviados
    })
    
@login_required
def publicar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    # Verifica se o usuário é colaborador confirmado
    convite = ConviteColaboracao.objects.filter(material=material, destinatario=request.user, status='aceito').first()
    if convite:
        # Confirma colaboração
        material.colaboradores_confirmados.add(request.user)
        # Atualiza o campo autor com os dois nomes
        autor_principal = material.usuario.username
        colaborador = request.user.username

        # Evita duplicação se o colaborador for o mesmo que o autor
        if autor_principal != colaborador:
            material.autor = f"{autor_principal} e {colaborador}"
        else:
            material.autor = autor_principal

        material.status = 'publicado'
        material.data_compartilhado = timezone.now()
        material.save()

        messages.success(request, "Material publicado com sucesso!")
        return redirect('meus_materiais')
    else:
        messages.error(request, "Você não tem permissão para publicar este material.")
        return redirect('convites')

