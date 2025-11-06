from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import User, Perfil
from django.contrib.auth.forms import PasswordChangeForm

class FormCadastro(UserCreationForm):
    first_name = forms.CharField(label='Nome', max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class FormPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['bio', 'cidade', 'estado', 'data_nascimento', 'telefone', 'avatar']
        labels = {
            'bio': 'Biografia',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'data_nascimento': 'Data de Nascimento',
            'telefone': 'Telefone',
            'avatar': 'Avatar'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AlterarSenhaForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Senha atual:",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
