from django.contrib.auth.decorators import login_required

# Formularios
from django.core.context_processors import csrf
from django.template import RequestContext

# General HTML
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# Manejo de Informacion de esta aplicacion
from datetime import datetime
from app_emergencia.forms import *

# Create your views here.
@login_required(login_url='/')
def paciente_perfil(request,idP):
    p = get_object_or_404(Paciente,pk=idP)
    ea = Emergencia.objects.filter(paciente=p)
    ea = ea[0]
    es = Emergencia.objects.filter(paciente=p)
    info = {'p':p,'ea':ea,'es':es}
    return render_to_response('perfil.html',info,context_instance=RequestContext(request))

@login_required(login_url='/')
def reporte_triage(request,idP):
    p = get_object_or_404(Paciente,pk=idP)
    ea = Emergencia.objects.filter(paciente=p)
    ea = ea[0]
    es = Emergencia.objects.filter(paciente=p)
    info = {'p':p,'ea':ea,'es':es}
    return render_to_response('reporteTriage.html',info,context_instance=RequestContext(request))

