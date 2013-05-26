from django import forms
from models import *
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.forms.widgets import RadioSelect
COD_TELEFONICOS = (
  ('0212','0212'),
  ('0412','0412'),
  ('0414','0414'),
  ('0424','0424'),
  ('0416','0416'),
  ('0426','0426'),
  )

class AgregarEmergenciaForm(forms.Form):
    cedula           = forms.CharField(max_length=9)
    nombres          = forms.CharField(max_length=64)
    apellidos        = forms.CharField(max_length=64)
    sexo             = forms.ChoiceField(choices=SEXO)
    fecha_nacimiento = forms.DateField()
    cod_cel          = forms.ChoiceField(choices=COD_TELEFONICOS)
    num_cel          = forms.CharField(max_length=7)
    email            = forms.EmailField(max_length=64)
    direccion        = forms.CharField(max_length=128)
    cod_tlf_casa     = forms.ChoiceField(choices=COD_TELEFONICOS)
    num_tlf_casa     = forms.CharField(max_length=7)    
    contacto_nombre  = forms.CharField(max_length=64)
    contacto_cod_tlf = forms.ChoiceField(choices=COD_TELEFONICOS)
    contacto_num_tlf = forms.CharField(max_length=11)
    ingreso          = forms.DateTimeField()
    
class calcularTriageForm(forms.Form):
    fecha         = forms.DateTimeField()
    motivo        = forms.ModelChoiceField(required=False,queryset=Motivo.objects.exclude(nombre__startswith=" "))
    area          = forms.ModelChoiceField(required=False,queryset=AreaEmergencia.objects.exclude(nombre__startswith=" "))
    ingreso       = forms.CharField(required=False,max_length=1,widget=forms.Select(choices=ICAUSA))
    
    atencion      = forms.NullBooleanField()
    esperar       = forms.NullBooleanField()
    recursos      = forms.IntegerField(required=False,widget=forms.Select(choices=RECURSOS))
    
    signos_tmp    = forms.FloatField(required=False)
    signos_fc     = forms.FloatField(required=False)
    signos_fr     = forms.IntegerField(required=False)
    signos_ta     = forms.IntegerField(required=False)
    signos_saod   = forms.FloatField(required=False)
    signos_motor  = forms.IntegerField(required=False,widget=forms.Select(choices=RMOTORA))
    signos_ocular = forms.IntegerField(required=False,widget=forms.Select(choices=ROCULAR))
    signos_verbal = forms.IntegerField(required=False,widget=forms.Select(choices=RVERBAL))
    signos_dolor  = forms.IntegerField(required=False,widget=forms.Select(choices=EDOLOR))
