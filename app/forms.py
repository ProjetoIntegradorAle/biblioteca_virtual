from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['titulo', 'descricao', 'tipo', 'arquivo']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'tipo': 'Tipo',
            'arquivo': 'Arquivo'
        }
        