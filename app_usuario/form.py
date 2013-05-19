from django import forms
from models import *

class IniciarSesionForm(forms.Form):
    unombre = forms.CharField(max_length=64)
    uclave  = forms.CharField(max_length=32,widget=forms.PasswordInput())
