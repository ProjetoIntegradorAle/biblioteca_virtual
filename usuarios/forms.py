from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Perfil
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
User = get_user_model()

class FormCadastro(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nome'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Endereço de email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuário'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmação de senha'}))

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
