from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext


# modelos de la base de datos
from django.db import models
from app_paciente.models import *
from app_usuario.models import * 


from django.contrib.auth import login, logout, authenticate # ver
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
# General HTML


from django.http import HttpResponse, HttpResponseRedirect

# Manejo de Informacion de esta aplicacion
from datetime import datetime
from models import *
from app_emergencia.models import *
# from forms import *


@login_required(login_url='/')
def atencion_atencion(request,id_emergencia):
	#emer    = get_object_or_404(Emergencia,id=id_emergencia)
    emer = Emergencia.objects.get(id=id_emergencia)
    medico = request.user
    ctx    = {'emergencia':emer,'medico':medico}
    return render_to_response('atencion_Plan.html',ctx,context_instance=RequestContext(request))


@login_required(login_url='/')
def atencion_enfermedad(request,id_emergencia,perfil):
    #emer    = get_object_or_404(Emergencia,id=id_emergencia)
    medico  = request.user
    emer = "emergencia"
    emer    = get_object_or_404(Emergencia,id=id_emergencia)
    ctx     = {'emergencia':emer,'medico':medico}
    return render_to_response('atencion_Plan.html',ctx,context_instance=RequestContext(request))


@login_required(login_url='/')
def atencion_indicaciones(request,id_emergencia,perfil):
    #emer    = get_object_or_404(Emergencia,id=id_emergencia)
    medico  = request.user
    emer = "emergencia"
    emer    = get_object_or_404(Emergencia,id=id_emergencia)
    ctx     = {'emergencia':emer,'medico':medico}
    return render_to_response('atencion_ind.html',ctx,context_instance=RequestContext(request))

@login_required(login_url='/')
def atencion_diagnostico(request,id_emergencia,perfil):
    #emer    = get_object_or_404(Emergencia,id=id_emergencia)
    medico  = request.user
    emer = "emergencia"
    emer    = get_object_or_404(Emergencia,id=id_emergencia)
    ctx     = {'emergencia':emer,'medico':medico}
    return render_to_response('atencion_diag.html',ctx,context_instance=RequestContext(request))

