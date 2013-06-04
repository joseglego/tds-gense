# -*- encoding: utf-8 -*-

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

############## Indicacion Terapeutica ################
IND_TER =(
  ('oral','Tratamiento Via Oral'),
  ('endov','Tratamiento Endovenoso'),
  ('neb','Nebulizacion'),
  ('Sutura de Herida','Sutura de Herida'),
  ('Inmovilizacion','Inmovilizacion'),
  ('rem','Remocion de Cuerpo Extraño'),
  ('catVen','Cateterizacion de Via Venosa Central'),
  ('sondajeNO','Sondaje Naso/Orogastrica'),
  ('sondajeV','Sondaje Vesical'),
  ('abseso','Drenaje de Abseso'),
  ('otro','Otro'),
  )


############## Indicacion Diagnostica Lab #############
DIAG_LAB = (
  ('hem','Hematologia Completa'),
  ('quim','Quimica Sanguinea'),
  ('elect','Electrolitos'),
  ('perfilC','Perfil de Coagulacion'),
  ('serol','Serologia'),
  ('marc','Marcadores Tumorales'),
  ('perfilH','Perfil Hormonal'),
  ('perfilI','Perfil Isquemico'),
  ('uroana','UroAnalisis'),
  ('copro','Coproanalisis'),
  )

############ Indicacion Diagnostica Micro #############
DIAG_MICRO= (
  ('hemo','Hemocultivo'),
  ('uroc','Urocultivo'),
  ('coproc','Coprocultivo'),
  ('exuF','Exudado Faringeo'),
  )

####### Indicacion Diagnostica Imagenologia ##########
DIAG_IMG= (
  ('rad','Radiografia'),
  ('ultra','Ultrasonido'),
  ('ultraD','Ultrasonido Doppler'),
  ('tomoAC','Tomografia Axial Computarizada'),
  ('resoMN','Resonancia Magnetica Nuclear'),
  )

############ Indicacion Diagnostica Endos #############
DIAG_END= (
  ('eds','Endoscopia Digestiva Superior'),
  ('edi','Endoscopia Digestiva Inferior'),
  ('ente','Enteroscopia'),
  ('pancre','Pancreratocolangiografia Retrogada Endoscopica'),
  ('resoMN','Resonancia Magnetica Nuclear'),
  )

################ Tipo Antecedente ####################
TIPO_ANT =(
  ('hipertension','Hipertension Arterial'),
  ('diabetes','Diabetes'),
  ('alergia','Alergia'),
  ('otros','Otros'),
  )

############ Diagnosticos Definitivos #################
TABLA_DIAG = (
  ('lista1','lista1'),
  ('lista2','lista2'),
  ('lista3','lista3'),
  )

############ Gestion Egresos #################
TABLA_DEST = (
  ('admision','Admision'),
  ('egreso','Egreso'),
  ('referencia','Referencia a especialista'),
  ('traslado','Traslado'),
  ('muerto','Muerte'),
  )

TABLA_AREADM = (
  ('hospital','Hospitalizacion'),
  ('quiro','Quirofano'),
  ('hemo','Hemodinamia'),
  ('parto','Sala de Parto'),
  ('intensivo','Unidad de Cuidados Intensivos'),
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


##################################################### FORMS ATENCION
class AgregarAntecedentesForm(forms.Form):
    nombreAnt = forms.ChoiceField(choices=TIPO_ANT)
    alergia   = forms.CharField(max_length=64)
    otro      = forms.CharField(max_length=64)
    narrativa = forms.CharField(widget=forms.Textarea)

# Agregar indicacion terapeutica
class AgregarIndTerapeuticaForm(forms.Form):
    nombreT    = forms.ChoiceField(choices=IND_TER)
    otroT      = forms.CharField(max_length=64)

# Agregar indicacion diagnostica Laboratorio
class AgregarIDLabForm(forms.Form):
    nombreDL    = forms.ChoiceField(choices=DIAG_LAB)
    otroDL      = forms.CharField(max_length=64)

# Agregar indicacion diagnostica Microbiologia
class AgregarIDMicroForm(forms.Form):
    nombreD    = forms.ChoiceField(choices=DIAG_MICRO)

# Agregar indicacion diagnostica Imagenologia
class AgregarIDImageForm(forms.Form):
    nombreD    = forms.ChoiceField(choices=DIAG_IMG)

# Agregar indicacion diagnostica Endoscopico
class AgregarIDEndosForm(forms.Form):
    nombreD    = forms.ChoiceField(choices=DIAG_END)


class AgregarDiagnosticoForm(forms.Form):
    diagnostico       = forms.ChoiceField(choices=TABLA_DIAG)
    destino           = forms.ChoiceField(choices=TABLA_DEST)
    area_admision     = forms.ChoiceField(choices=TABLA_AREADM)
    fecha_traslado    = forms.DateTimeField()
    fecha_indicacion  = forms.DateTimeField()

############################################################ Termina Forms Atencion