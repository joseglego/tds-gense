# -*- encoding: utf-8 -*-

from django.db import models
from app_paciente.models import *
from app_usuario.models import * 
from app_enfermedad.models import * 

# Create your models here.
AEMERGENCIA = (
    ('0','Real'),
    ('1','Referencia'),
)

ICAUSA = (
    ('0','No Violento'),
    ('1','Colision de Vehiculos'),
    ('2','Arrollamiento'),
    ('3','Herido por Arma Blanca'),
    ('4','Herido por Arma de Fuego'),
    ('5','Caida de Altura'),
    ('6','Intoxicacion'),
    ('7','Efecto Adverso a Medicamento'),
)

AFIRMACION = (
    (0,"No"),
    (1,"Si"),
)

RECURSOS = (
    (1,"Ninguno"),
    (2,"Uno"),
    (3,"Muchos"),
)

AVPU = (
    ("A","A - Alerta y ubicado en espacio y tiempo"),
    ("V","V - Responde ante ordenes verbales"),
    ("P","P - Responde a estimulos doloros"),
    ("U","U - Inconciente"),
)
EDOLOR = (
    (-1,"---------------"),
    (0,"No hay dolor"),
    (1,"1"),
    (2,"2"),
    (3,"3"),
    (4,"4"),
    (5,"5"),
    (6,"6"),
    (7,"7"),
    (8,"8"),
    (9,"9"),
    (10,"10"),
)
class AreaEmergencia(models.Model):
    tipo   = models.CharField(max_length=1,choices=AEMERGENCIA)
    nombre = models.CharField(max_length=48)
    def __unicode__(self):
        return "%s" % self.nombre

class AreaAdmision(models.Model):
    nombre = models.CharField(max_length=48)
    def __unicode__(self):
        return "%s" % self.nombre

class Cubiculo(models.Model):
    nombre = models.CharField(max_length=48)
    area   = models.ForeignKey(AreaEmergencia)
    def __unicode__(self):
        return "%s" % self.nombre

class Destino(models.Model):
    nombre = models.CharField(max_length=48)
    def __unicode__(self):
        return "%s" % self.nombre

class Motivo(models.Model):
    nombre = models.CharField(max_length=48)
    def __unicode__(self):
        return "%s" % self.nombre

class Emergencia(models.Model):
    paciente         = models.ForeignKey(Paciente)
    responsable      = models.ForeignKey(Usuario,related_name="A cargo")
    ingreso          = models.ForeignKey(Usuario,related_name="Ingresado por")
    hora_ingreso     = models.DateTimeField()
    hora_ingresoReal = models.DateTimeField(auto_now_add=True)
    hora_egreso      = models.DateTimeField(blank=True,null=True)
    hora_egresoReal  = models.DateTimeField(blank=True,null=True)
    egreso           = models.ForeignKey(Usuario,related_name="De alta por",blank=True,null=True)
    destino          = models.ForeignKey(Destino,blank=True,null=True)
    def __unicode__(self):
        return "%s - %s" % (self.id,self.paciente)

    def triages(self):
        triages = Triage.objects.filter(emergencia=self.id).order_by("fechaReal")
        return triages

    def triage(self):
        triage = 0
        triages = self.triages()
        if triages:
            triage = triages[0].nivel
        return triage

    def fecha_triage(self):
        triages = self.triages()
        fecha = "No se ha tomado signos vitales aún"
        if triages:
            if triages[0].fecha:
                fecha = triages[0].fecha.strftime("%H:%M del %d/%m/%y")
        return fecha

    def atendido(self):
        atendido = False
        atenciones = Atencion.objects.filter(emergencia=self.id)
        if len(atenciones) > 0:
            atendido = True
        return atendido
    def atenciones(self):
        atenciones = Atencion.objects.filter(emergencia=self.id).order_by("fechaReal")
        return atenciones
    def horaR(self):
        return self.hora_ingreso.strftime("%H:%M del %d/%m/%y")

class ComentarioEmergencia(models.Model):
    emergencia = models.ForeignKey(Emergencia)
    comentario = models.CharField(max_length=512)

class Admision(models.Model):
    emergencia       = models.ForeignKey(Emergencia)
    area             = models.ForeignKey(AreaAdmision)
    hora_ingreso     = models.DateTimeField(null=True,blank=True)
    hora_ingresoReal = models.DateTimeField(null=True,blank=True)

class Triage(models.Model):
    emergencia     = models.ForeignKey(Emergencia)
    medico         = models.ForeignKey(Usuario)
    fecha          = models.DateTimeField(blank=True,null=True)
    fechaReal      = models.DateTimeField(auto_now_add=True)
    
    motivo         = models.ForeignKey(Motivo,blank=True)
    areaAtencion   = models.ForeignKey(AreaEmergencia,blank=True)
    ingreso        = models.CharField(max_length=1,blank=True,choices=ICAUSA)
    
    atencion       = models.BooleanField(blank=True)
    esperar        = models.BooleanField(blank=True)
    recursos       = models.IntegerField(choices=RECURSOS,blank=True)
    
    # Valores a tomar
    signos_tmp     = models.FloatField(default=0,blank=True)
    signos_fc      = models.FloatField(default=0,blank=True)
    signos_fr      = models.IntegerField(default=0,blank=True)
    signos_pa      = models.IntegerField(default=0,blank=True)
    signos_pb      = models.IntegerField(default=0,blank=True)
    signos_saod    = models.FloatField(default=0,blank=True)

    # Otros Datos Importantes
    signos_avpu    = models.CharField(max_length=1,blank=True)
    signos_dolor   = models.IntegerField(default=0,blank=True)

    # Resultado de Triage
    nivel          = models.IntegerField()
    def __unicode___(self):
        return "Triaje %s" % self.id

    def fechaR(self):
        self.fecha.strftime("%H:%M del %d/%m/%y")

class ComentarioTriage(models.Model):
    triage = models.ForeignKey(Triage)
    comentario = models.CharField(max_length=512)

class Atencion(models.Model):
    emergencia     = models.ForeignKey(Emergencia)
    medico         = models.ForeignKey(Usuario)
    fecha          = models.DateTimeField()
    fechaReal      = models.DateTimeField(auto_now_add=True)
    area_atencion  = models.CharField(max_length=1)
 
class ComentarioAtencion(models.Model):
    atencion = models.ForeignKey(Atencion)
    comentario = models.CharField(max_length=512)

#_------------------------------------ Cambios Requerimientos 29_6
#----------------------------------Diagnostico Definitivo
class Diagnostico(models.Model):
    nombreD = models.CharField(max_length=512)
    def __unicode__(self):
        return "%s" % (self.nombreD)

class EstablecerDiag(models.Model):
    atencion = models.ForeignKey(Atencion)
    diagnostico = models.ForeignKey(Diagnostico)
    valoracion_esp = models.CharField(max_length=50)

class Indicacion(models.Model):
    nombre = models.CharField(max_length=128, blank=False)
    tipo   = models.CharField(max_length=40, blank=False)
    def __unicode__(self):
        # return "TIPO:%s- NOMBRE:%s" % (self.tipo,self.nombre)
        return "%s" % (self.nombre)

class Asignar(models.Model):
    emergencia = models.ForeignKey(Emergencia)
    indicacion = models.ForeignKey(Indicacion)
    persona    = models.ForeignKey(Usuario)
    fecha      = models.DateTimeField()
    fechaReal  = models.DateTimeField()
    def __unicode__(self):
        return "Paciente:%s- Nombre:%s- Tipo:%s" % (self.emergencia.paciente.nombres,self.indicacion.nombre,self.indicacion.tipo)
    def dosisA(self):
        result = DosisAsignar.objects.filter(asignacion=self)
        #print "RESULTADO OBJETOS DOSIS ASIGNAR",result
        if result:
            return "%s" %(result[0].dosis)
        else: 
            return "%s" % ("no hay dosis")

    def horaA(self):
        return self.fechaReal.strftime("%d/%m/%y a las %H:%M:%S")

# Especificaciones para las indicaciones de Dietas
class EspDieta(models.Model):
    asignacion       = models.ForeignKey(Asignar)
    observacion      = models.CharField(max_length=512,blank=True)
    def __unicode__(self):
        return "Paciente:%s- Dosis:%s" % (self.asignacion.emergencia.paciente.nombres,self.observacion)

# Especificaciones para las indicaciones de Hidratacion
class EspHidrata(models.Model):
    asignacion   = models.ForeignKey(Asignar)
    volumen      = models.IntegerField(default=0,blank=True)
    vel_infusion = models.CharField(max_length=512,blank=True)
    complementos = models.CharField(max_length=512,blank=True)
    def __unicode__(self):
        return "Paciente:%s- Dosis:%s" % (self.asignacion.emergencia.paciente.nombres,self.volumen)

class CombinarHidrata(models.Model):
    hidratacion1 = models.ForeignKey(EspHidrata)
    hidratacion2 = models.ForeignKey(Indicacion)

# Especificaciones para las indicaciones de Medicamentos
class EspMedics(models.Model):
    asignacion = models.ForeignKey(Asignar)
    dosis    = models.FloatField(default=0,blank=True)
    tipo_conc = models.CharField(max_length=2,blank=True)
    # mg
    # gr
    # u
    # cc
    frecuencia = models.CharField(max_length=25,blank=True)
    tipo_frec = models.CharField(max_length=4,blank=True)

    # fijo
    # SOS
    via_admin = models.CharField(max_length=20,blank=True)

    # via endovenosa
    # via subcutanea
    # nebulizacion
    # transdermico
    # via rectal

# Agrega los detalles extras para el tipo de frecuencia de SOS
class tieneSOS(models.Model):
    espMed      = models.ForeignKey(EspMedics)
    situacion   = models.CharField(max_length=200,blank=True)
    comentario  = models.CharField(max_length=200,blank=True)

# Especificaciones para las indicaciones de Imagenologia
class EspImg(models.Model):
    asignacion      = models.ForeignKey(Asignar)
    parte_cuerpo    = models.CharField(max_length=20,blank=True)