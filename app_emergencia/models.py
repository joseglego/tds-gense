from django.db import models
from app_paciente.models import *
from app_usuario.models import * 

# Create your models here.
class Emergencia(models.Model):
    paciente         = models.ForeignKey(Paciente)
    responsable      = models.ForeignKey(Usuario,related_name="A cargo")
    ingreso          = models.ForeignKey(Usuario,related_name="Ingresado por")
    hora_ingreso     = models.DateTimeField()
    hora_ingresoReal = models.DateTimeField(auto_now_add=True)
    hora_egreso      = models.DateTimeField(blank=True,null=True)
    def __unicode__(self):
        return "%s - %s" % (self.id,self.paciente)
    def triage(self):
        triage = 0
        triages = Triage.objects.filter(emergencia=self.id).order_by("-fechaReal")
        if triages:
            triage = triages[0].nivel
        return triage

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

class Cuerpo(models.Model):
    nombre = models.CharField(max_length=1)

class Atencion(models.Model):
    emergencia     = models.ForeignKey(Emergencia)
    medico         = models.ForeignKey(Usuario)
    fecha          = models.DateTimeField()
    fechaReal      = models.DateTimeField(auto_now_add=True)
    area_atencion  = models.CharField(max_length=1)
    enfermedad     = models.CharField(max_length=256)

class Problema(models.Model):
    atencion    = models.ForeignKey(Atencion)
    cuerpo      = models.ForeignKey(Cuerpo)
    descripcion = models.CharField(max_length=256)
    
