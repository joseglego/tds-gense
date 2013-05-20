from django.db import models
from django.contrib.auth.models import User

SEXO = (
    ('1','Hombre'),
    ('2','Mujer'),
)

USUARIO = (
    ('0','Administrador'),
    ('1','Medico'),
    ('2','Enfermera'),
    ('3','Secretaria'),
)
# Create your models here.
class Usuario(User):
    cedula      = models.IntegerField(default=0, unique=True)
    tipo        = models.CharField(max_length=1,choices=USUARIO)
    sexo        = models.CharField(max_length=1,choices=SEXO)
    tlf_cel     = models.CharField(max_length=11)
    direccion   = models.CharField(max_length=128)
    tlf_casa    = models.CharField(max_length=11)
