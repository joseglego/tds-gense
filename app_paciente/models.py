# -*- encoding: utf-8 -*-

from django.db import models
from django.utils import timezone

SEXO = (
    (1,'Hombre'),
    (2,'Mujer'),
)

RELACION = (
    (1,'Esposo/a'),
    (2,'Pareja'),
    (3,'Papa'),
    (4,'Mama'),
    (5,'Hermano/a'),
    (6,'Familiar'),
    (7,'Amigo/a'),
    (8,'Entorno Laboral'),
    (9,'Conocido'),
    (10,'Misma Comunidad'),
    (11,'No hay nexo'),
)

# Create your models here.
class Paciente(models.Model):
    cedula           = models.CharField(max_length=9,default=0)
    nombres          = models.CharField(max_length=64)
    apellidos        = models.CharField(max_length=64)
    sexo             = models.IntegerField(choices=SEXO)
    fecha_nacimiento = models.DateField()
    tlf_cel          = models.CharField(max_length=11)
    email            = models.CharField(max_length=64)
    direccion        = models.CharField(max_length=128)
    tlf_casa         = models.CharField(max_length=11)

    contacto_rel     = models.IntegerField(choices=RELACION)
    contacto_nom     = models.CharField(max_length=64)
    contacto_tlf     = models.CharField(max_length=11)

    foto = models.ImageField(upload_to="/home/jlego/tds-gense/media/img/pacientes",blank=True)
    signos_tmp     = models.FloatField(default=0,blank=True)
    signos_fc      = models.FloatField(default=0,blank=True)
    signos_fr      = models.IntegerField(default=0,blank=True)
    signos_pa      = models.IntegerField(default=0,blank=True)
    signos_pb      = models.IntegerField(default=0,blank=True)
    signos_saod    = models.FloatField(default=0,blank=True)
    def __unicode__(self):

        return "%s, %s" % (self.apellidos,self.nombres)

    def edad(self):
        edad = timezone.datetime.now().year - self.fecha_nacimiento.year
        mes = timezone.datetime.now().month - self.fecha_nacimiento.month
        if mes < 0:
            edad = edad -1
        elif mes == 0:
            dia = timezone.datetime.now().day - self.fecha_nacimiento.day
            if dia < 0:
                edad = edad -1
        return edad

    def meses(self):
        meses = (timezone.datetime.now().year - self.fecha_nacimiento.year)*12
        mes = timezone.datetime.now().month - self.fecha_nacimiento.month
        dia = timezone.datetime.now().day - self.fecha_nacimiento.day
        if dia < 0:
            mes = - 1
        meses = meses + mes        
        return abs(meses)

    def sexoR(self):
        resp = "Hombre"
        if (self.sexo == 2):
            resp = "Mujer"
        return resp

    def relacion(self):
        relaciones = [i[1] for i in RELACION if i[0] == self.contacto_rel]
        relacion = relaciones[0]
        return relacion

    def src_foto(self):
        resp = "/static/img/pacientes/hombre.png"
        if self.foto:
            resp="/foto/real"
        else:
            if (self.sexo == 2):
                resp = "/static/img/pacientes/mujer.png"
        return resp
                
class Antecedente(models.Model):
    nombre = models.CharField(max_length=64)

class Pertenencia(models.Model):
    paciente    = models.ForeignKey(Paciente)
    antecedente = models.ForeignKey(Antecedente)


class ComentarioPertenencia(models.Model):
    pertenencia = models.ForeignKey(Pertenencia)
    informacion = models.CharField(max_length=512)

