from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['autor', 'descricao', 'titulo', 'tipo', 'arquivo']
