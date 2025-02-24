from django import forms
from .models import Material, MeuModelo

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['titulo', 'descricao', 'autor', 'tipo', 'arquivo']

class MeuModeloForm(forms.ModelForm):
    class Meta:
        model = MeuModelo
        fields = ['image']
        