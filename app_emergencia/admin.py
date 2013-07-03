# -*- encoding: utf-8 -*-

from app_emergencia.models import *
from django.contrib import admin

admin.site.register(Emergencia)
admin.site.register(Triage)
admin.site.register(Motivo)
admin.site.register(AreaEmergencia)
admin.site.register(AreaAdmision)
admin.site.register(Cubiculo)
admin.site.register(Destino)
admin.site.register(Atencion)
admin.site.register(Indicacion)
admin.site.register(Asignar)
admin.site.register(EspDieta)


