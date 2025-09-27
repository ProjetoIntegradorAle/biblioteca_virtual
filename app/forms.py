from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    email_colaborador = forms.EmailField(
        required=False,
        label="E-mail do colaborador",
        widget=forms.EmailInput(attrs={'placeholder': 'Digite o e-mail do colaborador'})
    )

    class Meta:
        model = Material
        fields = ['titulo','descricao','tipo','arquivo','avaliacoes_habilitadas','colaboracao_habilitada']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'tipo': 'Tipo',
            'arquivo': 'Arquivo',
            'avaliacoes_habilitadas': 'Habilitar Avaliações',
            'colaboracao_habilitada': 'Habilitar Colaboração',
        }
