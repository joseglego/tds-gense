# -*- encoding: utf-8 -*-

from django import forms
from models import *
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

ATENCION = (
  (True,'Si'),
  (False,'No'),
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
    ingreso          = forms.DateTimeField(label="Hora y Fecha de Ingreso")
    cedula           = forms.CharField(label="Número de Cédula",max_length=9)
    nombres          = forms.CharField(label="Nombres", max_length=64)
    apellidos        = forms.CharField(label="Apellidos", max_length=64)
    sexo             = forms.ChoiceField(label="Sexo", choices=SEXO,required=False)
    fecha_nacimiento = forms.DateField(label="Fecha de Nacimiento",required=False)
    cel              = forms.CharField(label="Número de Teléfono Celular",max_length=11,required=False)
    email            = forms.EmailField(label="Correo Electrónico",max_length=64,required=False)
    direccion        = forms.CharField(label="Dirección",max_length=128,required=False)
    tlf_casa         = forms.CharField(label="Número de Teleéfono de Habitación",max_length=11,required=False)    
    contacto_nombre  = forms.CharField(label="Nombre de la Persona de Contacto",max_length=64,required=False)
    contacto_rel     = forms.ChoiceField(label="Vínculo entre El Conacto y el Paciente",choices=RELACION,required=False)
    contacto_tlf     = forms.CharField(label="Número de Teléfono del Contacto",max_length=11,required=False)
    foto             = forms.ImageField(label="Foto",required=False)
    

class darAlta(forms.Form):
    destino  = forms.ModelChoiceField(label="Destino",queryset=Destino.objects.all())
    area     = forms.ModelChoiceField(label="Área de la Clínica a la que va",required=False,queryset=AreaAdmision.objects.all())
    darAlta  = forms.DateTimeField(label="Fecha y Hora en que se da De Alta")
    traslado = forms.DateTimeField(required=False)

class BuscarEmergenciaForm(forms.Form):
    cedula = forms.CharField(label="Número de Cédula",max_length=11,required=False)
    nombres = forms.CharField(label="Nombres",max_length=32,required=False)
    apellidos = forms.CharField(label="Apellidos",max_length=32,required=False)


class calcularTriageForm(forms.Form):
    fecha         = forms.DateTimeField(label="Fecha y hora a la que se realiza la Evaluación")
    motivo        = forms.ModelChoiceField(label="Motivo de Ingreso (Escala de Manchester)",required=False,queryset=Motivo.objects.exclude(nombre__startswith=" "))
    ingreso       = forms.CharField(label="Tipo de Ingreso",required=False,max_length=1,widget=forms.Select(choices=ICAUSA))
    
    signos_tmp    = forms.FloatField(label="Temperatura",required=False)
    signos_fc     = forms.FloatField(label="Pulsaciones",required=False)
    signos_fr     = forms.IntegerField(label="Ventilaciones",required=False)
    signos_pa     = forms.IntegerField(label="Presión Sistólica / Alta",required=False)
    signos_pb     = forms.IntegerField(label="Presión Diastólica / Baja",required=False)
    signos_saod   = forms.FloatField(label="Saturación de Oxígeno",required=False)
    signos_avpu   = forms.CharField(label="Valor Obtenido en Escala AVPU",required=False,widget=forms.RadioSelect(choices=AVPU))
    signos_dolor  = forms.IntegerField(label="Intensidad del Dolor",required=False,widget=forms.Select(choices=EDOLOR))


##################################################### FORMS ATENCION

# Enfermedad Actual:
class AgregarEnfActual(forms.Form):
    # narrativa = forms.CharField(max_length=512,widget=forms.widgets.Textarea(attrs={'rows':10, 'cols':400}))
    narrativa = forms.CharField(widget=forms.widgets.Textarea)
    def __init__(self, *args, **kwargs):
      super(AgregarEnfActual, self).__init__(*args, **kwargs)
      self.fields['narrativa'].label = ""

# Indicaciones - Dieta
class AgregarIndDietaForm(forms.Form):
  dieta     = forms.ModelChoiceField(queryset=Indicacion.objects.filter(tipo__iexact="dieta"),widget=forms.RadioSelect())
  observacion = forms.CharField(max_length=100,widget=forms.widgets.Textarea(attrs={'rows':5, 'cols':100}))
  def __init__(self, *args, **kwargs):
    super(AgregarIndDietaForm, self).__init__(*args, **kwargs)
    self.fields['dieta'].empty_label = None
    self.fields['dieta'].label = "Tipo de Dieta:"

# Indicaciones - Hidratacion
class AgregarIndHidrataForm(forms.Form):
  hidrata     = forms.ModelChoiceField(required=True,queryset=Indicacion.objects.filter(tipo__iexact="hidrata"),widget=forms.RadioSelect())
  combina = forms.CharField(max_length=5,widget=forms.RadioSelect(choices=ATENCION))
  combina_sol= forms.ModelChoiceField(required=False,queryset=Indicacion.objects.filter(tipo__iexact="hidrata"),widget=forms.RadioSelect())
  volumen = forms.FloatField(required=False)
  vel_inf = forms.CharField(max_length=30)
  complementos = forms.CharField(max_length=40)
  
  def __init__(self, *args, **kwargs):
    super(AgregarIndHidrataForm, self).__init__(*args, **kwargs)
    self.fields['hidrata'].empty_label = None
    self.fields['combina_sol'].empty_label = None
    #------------Para cambiar los labels-------------------#
    self.fields['hidrata'].label = "Tipo de Solución:"
    self.fields['combina'].label = "¿Desea combinar con otro tipo de solución?:"
    self.fields['combina_sol'].label = "Tipo de Solución Adicional:"
    self.fields['vel_inf'].label = "Velocidad de Infusión:"

# Indicaciones - Diagnosticas - Laboratorio
class AgregarIndLabForm(forms.Form):
  lab     = forms.ModelChoiceField(queryset=Indicacion.objects.filter(tipo__iexact="lab"),widget=CheckboxSelectMultiple)
  def __init__(self, *args, **kwargs):
    super(AgregarIndLabForm, self).__init__(*args, **kwargs)
    self.fields['lab'].empty_label = None
    self.fields['lab'].label = "Exámenes de Laboratorio:"

# Indicaciones - Diagnosticas - Imagenologia
class AgregarIndImgForm(forms.Form):
  imagen     = forms.ModelChoiceField(queryset=Indicacion.objects.filter(tipo__iexact="imagen"),widget=CheckboxSelectMultiple)
  def __init__(self, *args, **kwargs):
    super(AgregarIndImgForm, self).__init__(*args, **kwargs)
    self.fields['imagen'].empty_label = None
    self.fields['imagen'].label = "Tipos de exámenes:"

# Indicaciones - Diagnosticas - Est endoscopicos
class AgregarIndEndosForm(forms.Form):
  endoscopico     = forms.ModelChoiceField(queryset=Indicacion.objects.filter(tipo__iexact="endoscopico"),widget=CheckboxSelectMultiple)
  Otros = forms.CharField(max_length=200)
  def __init__(self, *args, **kwargs):
    super(AgregarIndEndosForm, self).__init__(*args, **kwargs)
    self.fields['endoscopico'].empty_label = None
    self.fields['endoscopico'].label = "Exámenes Endoscópicos:"