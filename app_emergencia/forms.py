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
    sexo             = forms.ChoiceField(choices=SEXO,required=False)
    fecha_nacimiento = forms.DateField(required=False)
    cod_cel          = forms.ChoiceField(choices=COD_TELEFONICOS,required=False)
    num_cel          = forms.CharField(max_length=7,required=False)
    email            = forms.EmailField(max_length=64,required=False)
    direccion        = forms.CharField(max_length=128,required=False)
    cod_tlf_casa     = forms.ChoiceField(choices=COD_TELEFONICOS,required=False)
    num_tlf_casa     = forms.CharField(max_length=7,required=False)    
    contacto_nombre  = forms.CharField(max_length=64,required=False)
    contacto_cod_tlf = forms.ChoiceField(choices=COD_TELEFONICOS,required=False)
    contacto_num_tlf = forms.CharField(max_length=11,required=False)
    ingreso          = forms.DateTimeField()

class darAlta(forms.Form):
    destino  = forms.ModelChoiceField(queryset=Destino.objects.all())
    area     = forms.ModelChoiceField(required=False,queryset=AreaAdmision.objects.all())
    darAlta  = forms.DateTimeField()
    traslado = forms.DateTimeField(required=False)
    
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
    signos_pa     = forms.IntegerField(required=False)
    signos_pb     = forms.IntegerField(required=False)
    signos_saod   = forms.FloatField(required=False)
    signos_avpu   = forms.CharField(required=False,widget=forms.Select(choices=AVPU))
    signos_dolor  = forms.IntegerField(required=False,widget=forms.Select(choices=EDOLOR))
