# Manejo de Sesion
from django.contrib.auth.decorators import login_required

# Formularios
from django.core.context_processors import csrf
from django.template import RequestContext

# General HTML
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

# Manejo de Informacion de esta aplicacion
from datetime import datetime
from models import *
from forms import *

def emergencia_listar(request):    
    lista = Emergencia.objects.filter(hora_egreso=None)
    info = {'lista':lista}
    return render_to_response('lista.html',info)

def emergencia_listarPacientes(request):    
    listaP = Emergencia.objects.all()
    info = {'listaP':listaP}
    return render_to_response('listaGeneral.html',info)

@login_required(login_url='/')
def emergencia_agregar(request):
    mensaje = ""
    if request.method == 'POST':
        form = AgregarEmergenciaForm(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            p_cedula           = pcd['cedula']
            p_nombres          = pcd['nombres']
            p_apellidos        = pcd['apellidos']
            p_sexo             = pcd['sexo']
            p_fecha_nacimiento = pcd['fecha_nacimiento']
            p_cel              = pcd['cod_cel'] + pcd['num_cel']
            p_email            = pcd['email']
            p_direccion        = pcd['direccion']
            p_tlf_casa         = pcd['cod_tlf_casa'] + pcd['num_tlf_casa']
            p_contacto_nombre  = pcd['contacto_nombre']
            p_contacto_tlf     = pcd['contacto_cod_tlf'] + pcd['contacto_num_tlf']
            prueba = Paciente.objects.filter(cedula=p_cedula)
            if not prueba:
                p = Paciente(cedula=p_cedula,nombres=p_nombres,apellidos=p_apellidos,sexo=p_sexo,fecha_nacimiento=p_fecha_nacimiento,tlf_cel=p_cel,email=p_email,direccion=p_direccion,tlf_casa=p_tlf_casa,contacto_nom=p_contacto_nombre,contacto_tlf=p_contacto_tlf)
                p.save()
                e_ingreso = Usuario.objects.get(username=request.user)
                e_responsable= e_ingreso
                e_horaIngreso = pcd['ingreso']
                e_horaIngresoReal = datetime.now()
                e = Emergencia(paciente=p,responsable=e_responsable,ingreso=e_ingreso,hora_ingreso=e_horaIngreso,hora_ingresoReal=e_horaIngresoReal,hora_egreso=None)
                e.save()
                return redirect('/')
            else:
                mensaje = "Ya hay un paciente registrado con esa cedula"                
        info = {'form':form,'mensaje':mensaje}
        return render_to_response('agregarPaciente.html',info,context_instance=RequestContext(request))
    form = AgregarEmergenciaForm()
    info = {'form':form}
    return render_to_response('agregarPaciente.html',info,context_instance=RequestContext(request))

@login_required(login_url='/')
def emergencia_aplicarTriage(request,idE,vTriage):
    emergencia = get_object_or_404(Emergencia,id=idE)
    medico = Usuario.objects.get(username=request.user)
    if ((medico.tipo == "1") or (medico.tipo == "2")):
        print "Entre"
        fechaReal  = datetime.now()
        if ((int(vTriage) >= 1) and (int(vTriage) <= 5)):
            print "Entre 2"
            t = Triage(emergencia = emergencia,medico=medico,fechaReal=fechaReal,nivel=vTriage)
            t.save()
            return redirect("/emergencia/listar")
    return redirect("/")

#@login_required(login_url='/')
#def emergencia_calcularTriage(request,idE):
#    mensaje = ""
#    if request.method == 'POST':
#        emergencia = get_object_or_404(Emergencia,id=idE)
#        medico = Usuario.objects.get(username=request.user)
        
