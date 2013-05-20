from django import forms
from models import *

COD_TELEFONICOS = (
  ('0212','0212'),
  ('0412','0412'),
  ('0414','0414'),
  ('0424','0424'),
  ('0416','0416'),
  ('0426','0426'),
  )

class IniciarSesionForm(forms.Form):
    unombre = forms.CharField(max_length=64)
    uclave  = forms.CharField(max_length=32,widget=forms.PasswordInput())

class SolicitarCuenta(forms.Form):
    cedula    = forms.IntegerField()
    nombres   = forms.CharField()
    apellidos = forms.CharField()
    tipo      = forms.CharField(max_digits=1,widget=forms.Select(choices=USUARIO))
    sexo      = forms.CharField(max_ditits=1,widget=forms.Select(choices=SEXO))
    cod_cel   = forms.ChoiceField(choices=COD_TELEFONICOS)
    num_cel   = forms.CharField(max_length=7)
    direccion = forms.CharField(max_length=128)
    cod_casa  = forms.ChoiceField(choices=COD_TELEFONICOS)
    num_casa  = forms.CharField(max_length=7)
    email     = forms.emailField()
    clave     = forms.CharField(widget=forms.PasswordInput())
    claveV    = forms.CharField(widget=forms.PasswordInput())

    


