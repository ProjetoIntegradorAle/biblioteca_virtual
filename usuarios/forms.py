from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import User, Perfil

class FormCadastro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar Perfil'))

class FormRecuperaSenha(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar Email de Recuperação'))

class FormRedefineSenha(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Redefinir Senha'))