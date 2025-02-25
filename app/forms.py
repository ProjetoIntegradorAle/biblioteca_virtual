from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['titulo', 'descricao', 'autor', 'tipo', 'arquivo']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'autor': 'Autor',
            'tipo': 'Tipo',
            'arquivo': 'Arquivo'
        }
        