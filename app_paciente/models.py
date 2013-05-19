from django.db import models
SEXO = (
    ('1','Hombre'),
    ('2','Mujer'),
)

# Create your models here.
class Paciente(models.Model):
    cedula           = models.CharField(max_length=9,default=0, unique=True)
    nombres          = models.CharField(max_length=64)
    apellidos        = models.CharField(max_length=64)
    sexo             = models.CharField(max_length=1,choices=SEXO)
    fecha_nacimiento = models.DateField()
    tlf_cel          = models.CharField(max_length=11)
    email            = models.CharField(max_length=64)
    direccion        = models.CharField(max_length=128)
    tlf_casa         = models.CharField(max_length=11)
    contacto_nom     = models.CharField(max_length=64)
    contacto_tlf     = models.CharField(max_length=11)
    def __unicode__(self):
        return "%s %s" % (self.apellidos,self.nombres)

class Antecedente(models.Model):
    nombre = models.CharField(max_length=64)

class Pertenencia(models.Model):
    paciente    = models.ForeignKey(Paciente)
    antecedente = models.ForeignKey(Antecedente)

class ComentarioPertenencia(models.Model):
    pertenencia = models.ForeignKey(Pertenencia)
    informacion = models.CharField(max_length=512)

