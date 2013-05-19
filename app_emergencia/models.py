from django.db import models
from app_paciente.models import *
from app_usuario.models import * 

# Create your models here.

class AreaEmergencia(models.Model):
    nombre = models.CharField(max_length=48)

class AreaEgreso(models.Model):
    nombre = models.CharField(max_length=48)

class Cubiculo(models.Model):
    nombre = models.CharField(max_length=48)
    area   = models.ForeignKey(AreaEmergencia)

class Destino(models.Model):
    nombre = models.CharField(max_length=48)

class Emergencia(models.Model):
    paciente         = models.ForeignKey(Paciente)
    responsable      = models.ForeignKey(Usuario,related_name="A cargo")
    ingreso          = models.ForeignKey(Usuario,related_name="Ingresado por")
    hora_ingreso     = models.DateTimeField()
    hora_ingresoReal = models.DateTimeField(auto_now_add=True)
    hora_egreso      = models.DateTimeField(blank=True,null=True)
    hora_egresoReal  = models.DateTimeField(auto_now_add=True)
    egreso           = models.ForeignKey(Usuario,related_name="De alta por",blank=True)
    destino          = models.ForeignKey(Destino,blank=True)
    def __unicode__(self):
        return "%s - %s" % (self.id,self.paciente)
    def triage(self):
        triage = 0
        triages = Triage.objects.filter(emergencia=self.id).order_by("-fechaReal")
        if triages:
            triage = triages[0].nivel
        return triage

class ComentarioEmergencia(models.Model):
    emergencia = models.ForeignKey(Emergencia)
    comentario = models.CharField(max_length=512)

class Admision(models.Model):
    emergencia       = models.ForeignKey(Emergencia)
    area             = models.ForeignKey(AreaEgreso)
    hora_ingreso     = models.DateTimeField()
    hora_ingresoReal = models.DateTimeField(auto_now_add=True)    

class Triage(models.Model):
    emergencia     = models.ForeignKey(Emergencia)
    medico         = models.ForeignKey(Usuario)
    fecha          = models.DateTimeField(blank=True,null=True)
    fechaReal      = models.DateTimeField(auto_now_add=True)
    areaAtencion   = models.CharField(max_length=1,blank=True)
    signos_tmp     = models.FloatField(default=0,blank=True)
    signos_fc      = models.FloatField(default=0,blank=True)
    signos_fr      = models.IntegerField(default=0,blank=True)
    signos_ta      = models.IntegerField(default=0,blank=True)
    signos_saod    = models.FloatField(default=0,blank=True)
    signos_glasgow = models.IntegerField(default=0,blank=True)
    signos_dolor   = models.IntegerField(default=0,blank=True)
#   motivo
    ingreso        = models.CharField(max_length=1,blank=True)
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
