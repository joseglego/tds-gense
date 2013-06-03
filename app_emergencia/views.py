# Manejo de Sesion
from django.contrib.auth import authenticate, login, logout
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
            prueba = Paciente.objects.filter(cedula=p_cedula,nombres=p_nombres,apellidos=p_apellidos)

            if len(prueba) == 0:
                p = Paciente(cedula=p_cedula,nombres=p_nombres,apellidos=p_apellidos,sexo=p_sexo,fecha_nacimiento=p_fecha_nacimiento,tlf_cel=p_cel,email=p_email,direccion=p_direccion,tlf_casa=p_tlf_casa,contacto_nom=p_contacto_nombre,contacto_tlf=p_contacto_tlf)
                p.save()
            else:
                p = prueba[0]
            e_activa = len(Emergencia.objects.filter(paciente=p).filter(hora_egreso__isnull=True))
            if e_activa == 0:
                e_ingreso = Usuario.objects.get(username=request.user)
                e_responsable= e_ingreso
                e_horaIngreso = pcd['ingreso']
                e_horaIngresoReal = datetime.now()
                e = Emergencia(paciente=p,responsable=e_responsable,ingreso=e_ingreso,hora_ingreso=e_horaIngreso,hora_ingresoReal=e_horaIngresoReal,hora_egreso=None)
                e.save()
                return redirect('/emergencia/listar')
            else:
                msj_tipo = "error"
                msj_info = "Ya este usuario esta en una emergencia. No puede ingresar a un usuario 2 veces a la emergencia"
        info = {'form':form,'msj_tipo':msj_tipo,'msj_info':msj_info}
        return render_to_response('agregarPaciente.html',info,context_instance=RequestContext(request))
    form = AgregarEmergenciaForm()
    info = {'form':form}
    return render_to_response('agregarPaciente.html',info,context_instance=RequestContext(request))

#@login_required(login_url='/')
def emergencia_darAlta(request,idE):
    emergencia = get_object_or_404(Emergencia,id=idE)
    medico = Usuario.objects.get(username=request.user)
    if (medico.tipo == "1"):
        if request.method == 'POST':
            form = darAlta(request.POST)
            if form.is_valid():
                pcd = form.cleaned_data
                f_destino  = pcd['destino']
                f_area     = pcd['area']
                f_darAlta  = pcd['darAlta']
                f_traslado = pcd['traslado']
                emergencia.egreso=medico
                emergencia.hora_egreso=f_darAlta
                emergencia.hora_egresoReal=datetime.now()
                emergencia.destino=f_destino
                emergencia.save()
            else:
                info = {'form':form,'emergencia':emergencia}
                return render_to_response('darAlta.html',info,context_instance=RequestContext(request))
        else:
            form = darAlta()
            info = {'form':form,'emergencia':emergencia}
            return render_to_response('darAlta.html',info,context_instance=RequestContext(request))    
    return redirect("/emergencia/listar")

@login_required(login_url='/')
def emergencia_aplicarTriage(request,idE,vTriage):
    emergencia = get_object_or_404(Emergencia,id=idE)
    medico = Usuario.objects.get(username=request.user)
    if ((medico.tipo == "1") or (medico.tipo == "2")):
        fechaReal  = datetime.now()
        if ((int(vTriage) >= 1) and (int(vTriage) <= 5)):
            motivo = Motivo.objects.get(nombre__startswith=" Ingreso")
            area = AreaEmergencia.objects.get(nombre__startswith=" Ingreso")
            recursos = 0
            t = Triage(emergencia = emergencia,medico=medico,fechaReal=fechaReal,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=vTriage)
            t.save()
            return redirect("/emergencia/listar")
    return redirect("/")

@login_required(login_url='/')
def emergencia_calcularTriage(request,idE):
    mensaje = ""
    if request.method == 'POST':
        form = calcularTriageForm(request.POST)
        if form.is_valid():
            emergencia = get_object_or_404(Emergencia,id=idE)
            medico = Usuario.objects.get(username=request.user)
            pcd = form.cleaned_data
            f_fecha    = pcd['fecha']
            f_motivo   = pcd['motivo']
            f_area     = pcd['area']
            f_atencion = pcd['atencion']
            f_ingreso  = pcd['ingreso']
            f_esperar  = pcd['esperar']
            f_recursos = pcd['recursos']
            f_temp     = pcd['signos_tmp']
            f_fc       = pcd['signos_fc']
            f_fr       = pcd['signos_fr']
            f_pa       = pcd['signos_pa']
            f_pb       = pcd['signos_pb']
            f_saod     = pcd['signos_saod']
            f_avpu     = pcd['signos_avpu']

            f_dolor    = pcd['signos_dolor']
            if (f_atencion == True):
                motivo = Motivo.objects.get(nombre__startswith=" Ingreso")
                area = AreaEmergencia.objects.get(nombre__startswith=" Ingreso")
                recursos = 0                
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=1)
                t.save()
                print "Caso 1"
                return redirect("/emergencia/listar")
            elif (f_atencion == False) and (f_esperar == False):
                motivo = Motivo.objects.get(nombre__startswith=" Ingreso")
                area = AreaEmergencia.objects.get(nombre__startswith=" Ingreso")
                recursos = 0               
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=2)
                t.save()
                print "Caso 2"
                return redirect("/emergencia/listar")
            elif (f_atencion == False) and (f_esperar == True) and (f_recursos ==1):
                motivo = Motivo.objects.get(nombre__startswith=" Salida")
                area = AreaEmergencia.objects.get(nombre__startswith=" Salida")
                recursos = f_recursos
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=5)
                t.save()
                print "Caso 3"
                return redirect("/emergencia/listar")
            elif (f_atencion == False) and (f_esperar == True) and (f_recursos ==2):
                motivo = Motivo.objects.get(nombre__startswith=" Salida")
                area = AreaEmergencia.objects.get(nombre__startswith=" Salida")
                recursos = f_recursos
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=4)
                t.save()
                print "Caso 4"
                return redirect("/emergencia/listar")
            else:
                print "Evaluar Todo"
                # Base
                p = emergencia.paciente
                fcAlta  = 100
                frAlta  = 20
                soBaja  = 92
                soMBaj  = 90
                tmpAlta = 40
                tmpMAlt = 41
                triage  = 5
                
                # Calculo de la edad - limites
                if (p.edad() < 3):
                    if ((p.edad() == 0) and (p.meses() < 3)):
                        fcAlta  = 180
                        frAlta  = 50
                        tmpAlta = 37
                        tmpMAlt = 38
                    else:
                        fcAlta  = 160
                        frAlta  = 40
                        tmpAlta = 39
                        tmpMAlt = 40
                elif ((p.edad() >= 3) and (p.edad() <= 8)):
                    fcAlta = 140
                    frAlta = 30

                # Evaluacion de Frecuencia Cardiaca
                if (f_fc > fcAlta):
                    triage = min(triage,2)
                    print "FC"
                else:
                    triage = min(triage,3)

                # Evaluacion de Frecuencia Respiratoria
                if (f_fr > frAlta):
                    triage = min(triage,2)
                    print "FR"
                else:
                    triage = min(triage,3)

                # Evaluacion de Saturacion de Oxigeno
                if (f_saod < soBaja):
                    triage = min(triage,2)
                    print "SAOD"

                # Condicion A, Lectura
                elif (f_saod < soMBaj):
                    triage = min(triage,1)
                else:
                    triage = min(triage,3)

                # Evaluacion de Temperatura
                if (f_temp == tmpAlta):
                    triage = min(triage,3)
                elif (f_temp == tmpMAlt):
                    print "TMP"
                    triage = min(triage,2)
                elif (f_temp > tmpMAlt):
                    triage = min(triage,1)
                
                # Condicion A, Lectura
                if ((f_avpu == 'U') or (f_avpu == 'P')):
                    triage = min(triage,1)
                
                # Condicion B, Lectura
                if (f_dolor > 7):
                    print "Dolor"
                    triage = min(triage,2)
                
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=f_motivo,areaAtencion=f_area,ingreso=f_ingreso,atencion=f_atencion,esperar=f_esperar,recursos=f_recursos,signos_tmp=f_temp,signos_fc=f_fc,signos_fr=f_fr,signos_pa=f_pb,signos_saod=f_saod,signos_avpu=f_avpu,signos_dolor=f_dolor,nivel=triage)
                t.save()
                return redirect("/emergencia/listar")
        else:
            print "Error 2"
    form = calcularTriageForm()
    info = {'form':form,'idE':idE}
    return render_to_response('calcularTriage.html',info,context_instance=RequestContext(request))
