# -*- encoding: utf-8 -*-

from django.db import models
from app_paciente.models import *
from app_usuario.models import * 

# Create your models here.
AEMERGENCIA = (
    ('0','Real'),
    ('1','Referencia'),
)

ICAUSA = (
    ('0','-------------------'),
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
    ("-1","--------"),
    (1,"Ninguno"),
    (2,"Uno"),
    (3,"Muchos"),
)

ROCULAR = (
    (-1,"-------------------"),
    (1,"Sin Apertura Ocular"),
    (2,"Al Dolor"),
    (3,"A la Voz"),
    (4,"Espontánea"),
)

RVERBAL = (
    (-1,"--------------------"),
    (1,"Sin Respuesta Verbal"),
    (2,"Sonidos"),
    (3,"Palabras"),
    (4,"Confuso"),
    (5,"Orientado"),
)

RMOTORA = (
    (-1,"----------------------"),
    (1,"Sin Respuesta Motora"),
    (2,"Respuesta en Extensión"),
    (3,"Respuesta en Flexión"),
    (4,"Retira Ante Estímulos"),
    (5,"Localiza Estímulos"),
    (6,"Obedece Órdenes"),
)

AVPU = (
    ("Z","---------------"),
    ("A","Alert - Alerta y ubicado en espacio y tiempo"),
    ("V","Verbal - Responde ante ordenes verbales"),
    ("P","Pain - Responde a estimulos doloros"),
    ("U","Unconscious - Inconciente"),
)
EDOLOR = (
    (-1,"---------------"),
    (0,"Sin Dolor"),
    (1,"Apenas Duele"),
    (2,"Leve"),
    (3,"Un Poco Molesto"),
    (4,"Moderado"),
    (5,"Intenso"),
    (6,"Severo"),
    (7,"Fuerte"),
    (8,"Muy Severo"),
    (9,"Muy Fuerte"),
    (10,"Intolerable"),
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
    def triage(self):
        triage = 0
        triages = Triage.objects.filter(emergencia=self.id).order_by("-fechaReal")
        if triages:
            triage = triages[0].nivel
        return triage
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

class ComentarioTriage(models.Model):
    triage = models.ForeignKey(Triage)
    comentario = models.CharField(max_length=512)

class Atencion(models.Model):
    emergencia     = models.ForeignKey(Emergencia)
    medico         = models.ForeignKey(Usuario)
    fecha          = models.DateTimeField()
    fechaReal      = models.DateTimeField(auto_now_add=True)
    area_atencion  = models.CharField(max_length=1)
    enfermedad     = models.CharField(max_length=256)   

class ComentarioAtencion(models.Model):
    atencion = models.ForeignKey(Atencion)
    comentario = models.CharField(max_length=512)

class CategoriaDeIndicacion(models.Model):
    nombre = models.CharField(max_length=128)

class Indicacion(models.Model):
    nombre = models.CharField(max_length=128)
    tipo   = models.CharField(max_length=1)

class IndicacionEsp(models.Model):
    indicacion = models.ForeignKey(Indicacion)
    categoria  = models.ForeignKey(CategoriaDeIndicacion)

class Asignar(models.Model):
    emergencia = models.ForeignKey(Emergencia)
    indicacion = models.ForeignKey(Indicacion)
    persona    = models.ForeignKey(Usuario)
    fecha      = models.DateTimeField()
    fechaReal  = models.DateTimeField()
    
class ComentarioAsignar(models.Model):
    asignacion = models.ForeignKey(Asignar)
    comentario = models.CharField(max_length=512)
