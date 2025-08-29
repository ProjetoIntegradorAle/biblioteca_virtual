from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['titulo', 'descricao', 'tipo', 'arquivo', 'avaliacoes_habilitadas', 'colaboracao_habilitada']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'tipo': 'Tipo',
            'arquivo': 'Arquivo',
            'avaliacoes_habilitadas': 'Habilitar Avaliações',
            'colaboracao_habilitada': 'Habilitar Colaboração',
        }
        