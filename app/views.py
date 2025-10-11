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
        
        # --- DEBUG PRINT 1: Ver o que o formulário enviou ---
        print("--- DADOS DO POST RECEBIDOS ---")
        print(request.POST)
        print("-------------------------------")

        if form.is_valid():
            novo_material = form.save(commit=False)
            novo_material.usuario = request.user
            novo_material.autor = request.user.username
            novo_material.status = 'rascunho'
            novo_material.save()

            colaboracao_habilitada = request.POST.get('colaboracao_habilitada')
            email_colaborador = request.POST.get('email_colaborador', '').strip() # .strip() remove espaços em branco

            # --- DEBUG PRINT 2: Ver os valores das variáveis ---
            print(f"Checkbox 'colaboracao_habilitada': {colaboracao_habilitada}")
            print(f"Campo 'email_colaborador': {email_colaborador}")

            # A condição é VERDADEIRA se o checkbox estiver marcado E o campo de email NÃO estiver vazio
            if colaboracao_habilitada and email_colaborador:
                print(">>> CONDIÇÃO DE COLABORAÇÃO ATENDIDA. Tentando criar convite...")
                try:
                    # Usamos 'iexact' para ignorar maiúsculas/minúsculas no email
                    colaborador = User.objects.get(email__iexact=email_colaborador)

                    # VERIFICAÇÃO IMPORTANTE: Não deixar o usuário convidar a si mesmo
                    if colaborador == request.user:
                        messages.warning(request, 'Você não pode convidar a si mesmo para colaborar.')
                        # Mesmo com o erro, o material já foi criado como rascunho
                        return redirect('meus_materiais')

                    # Cria o convite
                    ConviteColaboracao.objects.create(
                        material=novo_material,
                        remetente=request.user,
                        destinatario=colaborador
                    )

                    # Adiciona aos pendentes e atualiza o material
                    novo_material.colaboradores_pendentes.add(colaborador)
                    novo_material.colaboracao_habilitada = True
                    novo_material.status = 'aguardando'
                    novo_material.save()
                    messages.info(request, f'Convite de colaboração enviado para {colaborador.username}.')

                except User.DoesNotExist:
                    messages.warning(request, f'Colaborador com o email "{email_colaborador}" não foi encontrado.')
                    print(f">>> ERRO: Usuário com email '{email_colaborador}' não existe.")
            
            else:
                print(">>> CONDIÇÃO DE COLABORAÇÃO NÃO ATENDIDA. Publicando material diretamente.")
                novo_material.status = 'publicado'
                novo_material.save()
                messages.success(request, 'Material criado com sucesso!')
            
            return redirect('meus_materiais')
        
        else:
            messages.error(request, 'Erro ao criar material. Verifique os campos.')
    
    else:
        form = MaterialForm()

    # Corrigindo o warning da paginação
    materiais_criados = Material.objects.filter(usuario=request.user).order_by('-data_compartilhado')
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
def publicar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    # Verifica se o usuário é colaborador confirmado
    convite = ConviteColaboracao.objects.filter(material=material, destinatario=request.user, status='aceito').first()
    if convite:
        # Confirma colaboração
        material.colaboradores_confirmados.add(request.user)
        material.status = 'publicado'
        material.data_compartilhado = timezone.now()
        material.save()

        messages.success(request, "Material publicado com sucesso!")
        return redirect('meus_materiais')
    else:
        messages.error(request, "Você não tem permissão para publicar este material.")
        return redirect('convites')


# VIEWS PARA GERENCIAMENTO DE CONVITES DE COLABORAÇÃO


@login_required
def listar_convites(request):
    """
    Exibe os convites de colaboração recebidos e enviados pelo usuário logado.
    """
    print("--- A view 'listar_convites' foi executada! ---")
    convites_recebidos = ConviteColaboracao.objects.filter(
        destinatario=request.user
    ).order_by('-data_envio')
    
    convites_enviados = ConviteColaboracao.objects.filter(
        remetente=request.user
    ).order_by('-data_envio')

    print(f"Convites recebidos: {convites_recebidos.count()}")
    print(f"Convites enviados: {convites_enviados.count()}")
    
    context = {
        'convites_recebidos': convites_recebidos,
        'convites_enviados': convites_enviados
    }
    return render(request, 'config-templates/convites.html', context)


@login_required
def responder_convite(request, convite_id):
    """
    Processa a resposta (aceite ou recusa) a um convite de colaboração.
    """
    convite = get_object_or_404(ConviteColaboracao, id=convite_id, destinatario=request.user)

    if request.method == 'POST':
        resposta = request.POST.get('resposta') # 'aceito' ou 'negado'

        if resposta in ['aceito', 'negado']:
            convite.status = resposta
            convite.data_resposta = timezone.now()
            convite.save()
            
            material = convite.material
            # Remove o usuário da lista de pendentes em ambos os casos
            material.colaboradores_pendentes.remove(request.user)
            
            if resposta == 'aceito':
                # Adiciona à lista de confirmados se aceito
                material.colaboradores_confirmados.add(request.user)
                material.status = 'publicado' # Atualiza o status do material para publicado
                material.save()
                messages.success(request, f'Você aceitou colaborar no material "{material.titulo}".')
            else:
                messages.info(request, f'Você recusou colaborar no material "{material.titulo}".')
            
            return redirect('listar_convites')

    # Redireciona de volta se o método não for POST ou a resposta for inválida
    return redirect('listar_convites')
