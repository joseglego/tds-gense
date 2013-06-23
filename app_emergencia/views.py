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
from app_usuario.forms import *

#####################################################
#Imports Atencion
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from app_enfermedad.models import *
######################################################

def emergencia_listar_todas(request):   
    lista = Emergencia.objects.filter(hora_egreso=None)
    form = IniciarSesionForm()
    info = {'lista':lista,'form':form}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_triage(request):
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.atendido() == False]
    form = IniciarSesionForm()
    info = {'lista':lista,'form':form}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_sinclasificar(request):    
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.triage() == 0]
    form = IniciarSesionForm()
    info = {'lista':lista,'form':form}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_clasificados(request):    
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.triage() != 0 and i.atendido() == False]
    form = IniciarSesionForm()
    info = {'lista':lista,'form':form}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_atencion(request):
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.atendido() == True]
    form = IniciarSesionForm()
    info = {'lista':lista,'form':form}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

@login_required(login_url='/')
def paciente_perfil(request,idP):
    p = get_object_or_404(Paciente,pk=idP)
    ea = Emergencia.objects.filter(paciente=p)
    ea = ea[0]
    es = Emergencia.objects.filter(paciente=p)
    info = {'p':p,'ea':ea,'es':es}
    return render_to_response('perfil.html',info,context_instance=RequestContext(request))

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
            p_cel              = pcd['cel']
            p_email            = pcd['email']
            p_direccion        = pcd['direccion']
            p_tlf_casa         = pcd['tlf_casa']
            p_contacto_rel     = pcd['contacto_rel']
            p_contacto_nombre  = pcd['contacto_nombre']
            p_contacto_tlf     = pcd['contacto_tlf']
            prueba = Paciente.objects.filter(cedula=p_cedula,nombres=p_nombres,apellidos=p_apellidos)

            if len(prueba) == 0:
                p = Paciente(cedula=p_cedula,nombres=p_nombres,apellidos=p_apellidos,sexo=p_sexo,fecha_nacimiento=p_fecha_nacimiento,tlf_cel=p_cel,email=p_email,direccion=p_direccion,tlf_casa=p_tlf_casa,contacto_rel=p_contacto_rel,contacto_nom=p_contacto_nombre,contacto_tlf=p_contacto_tlf)
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
                return redirect('/emergencia/listar/todas')
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
    return redirect("/emergencia/listar/todas")

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
            return redirect("/emergencia/listar/todas")
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
                return redirect("/emergencia/listar/todos")
            elif (f_atencion == False) and (f_esperar == False):
                motivo = Motivo.objects.get(nombre__startswith=" Ingreso")
                area = AreaEmergencia.objects.get(nombre__startswith=" Ingreso")
                recursos = 0               
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=2)
                t.save()
                print "Caso 2"
                return redirect("/emergencia/listar/todas")
            elif (f_atencion == False) and (f_esperar == True) and (f_recursos ==1):
                motivo = Motivo.objects.get(nombre__startswith=" Salida")
                area = AreaEmergencia.objects.get(nombre__startswith=" Salida")
                recursos = f_recursos
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=5)
                t.save()
                print "Caso 3"
                return redirect("/emergencia/listar/todas")
            elif (f_atencion == False) and (f_esperar == True) and (f_recursos ==2):
                motivo = Motivo.objects.get(nombre__startswith=" Salida")
                area = AreaEmergencia.objects.get(nombre__startswith=" Salida")
                recursos = f_recursos
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=motivo,areaAtencion=area,recursos=recursos,nivel=4)
                t.save()
                print "Caso 4"
                return redirect("/emergencia/listar/todas")
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
                
                if (triage == 1) or (triage == 2):
                  f_area = AreaEmergencia.objects.get(nombre__startswith="Sala de")
                else:
                  f_area = AreaEmergencia.objects.get(nombre__startswith="Atenci")     
            
                t = Triage(emergencia = emergencia,medico=medico,fecha=f_fecha,motivo=f_motivo,areaAtencion=f_area,ingreso=f_ingreso,atencion=f_atencion,esperar=f_esperar,recursos=f_recursos,signos_tmp=f_temp,signos_fc=f_fc,signos_fr=f_fr,signos_pa=f_pb,signos_saod=f_saod,signos_avpu=f_avpu,signos_dolor=f_dolor,nivel=triage)
                paciente = emergencia.paciente
                paciente.signos_tmp = f_temp
                paciente.signos_fc = f_fc
                paciente.signos_fr = f_fr
                paciente.signos_pa = f_pa
                paciente.signos_pb = f_pb
                paciente.signos_saod = f_saod
                paciente.save()
                t.save()
                return redirect("/emergencia/listar/todas")
        else:
            print "Error 2"
    form = calcularTriageForm()
    info = {'form':form,'idE':idE}
    return render_to_response('calcularTriage.html',info,context_instance=RequestContext(request))

#########################################################
#                                                       #
#          Views para Casos de Uso de Atencion          #
#                                                       #      
#########################################################

# A cada una le paso el id de emergencia para mantener la 
# informacion constante en el sidebar izquierdo

#----------------------------------------------------- Funciones para generar Pdfs
def generar_pdf(html):
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def emergencia_descarga(request,id_emergencia):
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    #triages = Triage.objects.filter(emergencia=self.id).order_by("-fechaReal")
    #ctx = {'emergencia':emer,'triage':triage}
    # TERMINAR CONSULTAS PARA INGRESAR AL CONTEXTO
    ctx = {'emergencia':emer}
    html = render_to_string('historia_med.html',ctx, context_instance=RequestContext(request))
    return generar_pdf(html)

#---------------------------------Iniciara por default en la vista de antecedentes
@login_required(login_url='/')
def emergencia_atencion(request,id_emergencia):
    print "si entrar"
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    print "paciente",paci
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    mensaje = ""
    if request.method == 'POST':
        form = AgregarAntecedentesForm(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            p_nombre          = pcd['nombreAnt']
            p_alergia         = pcd['alergia']
            p_otro            = pcd['otro']
            # Agregar antecedente
            a = Antecedente.objects.filter(nombre=p_nombre)
            
            if not a:
                a1 = Antecedente(nombre=p_nombre)
                a1.save()
                perte1 = Pertenencia(paciente=paci,antecedente=a1)
                perte1.save()
            else:
                ant = a[0]
                perte = Pertenencia.objects.filter(paciente=paci,antecedente=ant)
                if not perte:
                    perte1 = Pertenencia(paciente=paci,antecedente=ant)
                    perte1.save()
                else:
                    mensaje="Antecedente ya existente"
                    info = {'form':form,'mensaje':mensaje}
                    return render_to_response('atencion_ant.html',info,context_instance=RequestContext(request))
        else:
            print "formulario invalido"
            mensaje="Formulario invalido"
            info = {'form':form,'mensaje':mensaje}
            return render_to_response('atencion_ant.html',info,context_instance=RequestContext(request))
    antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci)
    print "antecedentes",antecedentes
    form = AgregarAntecedentesForm()
    info = {'form':form,'emergencia':emer,'triage':triage,'antecedentes':antecedentes}
    return render_to_response('atencion_ant.html',info,context_instance=RequestContext(request))


#----------------------------------Gestion de Antecedentes en area de Atencion
@login_required(login_url='/')
def emergencia_antecedentes(request,id_emergencia):
    print "si entrar"
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    print "paciente",paci
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    mensaje = ""
    if request.method == 'POST':
        form = AgregarAntecedentesForm(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            p_nombre          = pcd['nombreAnt']
            p_alergia         = pcd['alergia']
            p_otro            = pcd['otro']
            # Agregar antecedente
            a = Antecedente.objects.filter(nombre=p_nombre)
            
            if not a:
                a1 = Antecedente(nombre=p_nombre)
                a1.save()
                perte1 = Pertenencia(paciente=paci,antecedente=a1)
                perte1.save()
            else:
                ant = a[0]
                perte = Pertenencia.objects.filter(paciente=paci,antecedente=ant)
                if not perte:
                    perte1 = Pertenencia(paciente=paci,antecedente=ant)
                    perte1.save()
                else:
                    mensaje="Antecedente ya existente"
                    antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci)
                    info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'antecedentes':antecedentes}
                    return render_to_response('atencion_ant.html',info,context_instance=RequestContext(request))
        else:
            print "formulario invalido"
            mensaje="Formulario invalido"
            antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci)
            info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'antecedentes':antecedentes}
            return render_to_response('atencion_ant.html',info,context_instance=RequestContext(request))
    antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci)
    print "antecedentes",antecedentes
    form = AgregarAntecedentesForm()
    info = {'form':form,'emergencia':emer,'triage':triage,'antecedentes':antecedentes}
    return render_to_response('atencion_ant.html',info,context_instance=RequestContext(request))


#--------------------------------Gestion de Enfermedad (Examen Fisico)
@login_required(login_url='/')
def emergencia_enfermedad(request,id_emergencia):#enfermedad
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    print "triage len", len(triage)
    origenes =  OrigenProblema.objects.filter()
    print "ORIGENES: ",origenes
    presentes = Presente.objects.filter()
    print "PRESENTES: ",presentes 
    triage = triage[0]
    causa  = 0
    parte_cuerpo = 0
    print "por aqui voy"
    atencion = Atencion.objects.filter(emergencia=id_emergencia)
    print "atencion", atencion[0].fecha
    print "atencion: ",len(atencion)
    if triage:
        print "triage: ",triage.id
        problema = Problema.objects.filter(atencion__id = atencion[0].id)
        problemas = Problema.objects.filter()
        c = Causa.objects.filter()#select_related('nombre', 'sintomas')
        print "LOS Causa: ",c
        print "LOS PROBLEMAS: ",problemas
        if problema:
            print "problema: ", len(problema), problema[0].nombre
            print "lista ", problema
            causa = Causa.objects.filter(origenproblema__problema__nombre = problema[0].nombre)
            if causa:
                print "causa: ",len(causa)
                parte_cuerpo = ParteCuerpo.objects.filter()
    ctx    = {'emergencia':emer,'triage':triage,'causa':causa,'parte_cuerpo':parte_cuerpo,'origen':origenes,'presente':presentes}
    return render_to_response('atencion_Plan.html',ctx,context_instance=RequestContext(request))


#--------------------------------Gestion de Indicaciones Terapeuticas
@login_required(login_url='/')
def emergencia_indicacionesT(request,id_emergencia):
    
    # FUNCION PARA MANIPULAR EL FORMULARIO Y PARA LISTAR LAS INDICACIONES Terapeuticas
    # Consultas para guardar abajo los objetos pertinentes
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    #usr = Usuario.objects.get(username=request.user)
    #print "usuario es:",usr
    ingreso = datetime.now()
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    #categoria = 0
    #indicaciones = Indicacion.objects.filter()
    indicaciones = Indicacion.objects.filter(asignar__emergencia = id_emergencia)
    print "indicaciones: ",indicaciones
    #form=""
    
    ###Codigo Form:
    mensaje = ""
    if request.method == 'POST':
        form = AgregarIndTerapeuticaForm(request.POST)
        print "Validez Formulario:",str(form.is_valid())
        #Print de inputs del formulario
        print "veo tipo:",form.cleaned_data['nombreT']
        print "veo nombre:",form.cleaned_data['otroT']
        if form.is_valid():
            pcd = form.cleaned_data
            p_nombre            = pcd['nombreT']
            p_otro              = pcd['otroT']
            #Agrego indicacion dependiendo del tipo
            print "veo nombre:",p_nombre
            print "veo otro:",p_otro
            
            indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = p_nombre)
            #print "indicaciones: ",len(indicaciones)
            if indicacionesQ:
                # Falta agregar Condicional cuando tengo indicaciones de tipo terapeutico q no tienen categoria
                mensaje = "Hay indicaciones con ese nombre"
                #OJO AQUI TENGO QUE PASARLE LA TABLA DE ASIGNAR para que pueda listar la hora
                info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones}
                return render_to_response('atencion_indT.html',info,context_instance=RequestContext(request))
            else:
                print "no hay elementos"
                #Agrego para ver si sirve
                print "Input p_tipo",p_nombre
                print "Input p_nombre",p_otro
                i = Indicacion(nombre=p_nombre,tipo="terapeutico")
                i.save()
                a = Asignar(emergencia=emer,indicacion=i,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                a.save()
                mensaje = "Guardado Exitosamente"
                
                #OJO AQUI TENGO QUE PASARLE LA TABLA DE ASIGNAR para que pueda listar la hora
                info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones}
                return render_to_response('atencion_indT.html',info,context_instance=RequestContext(request))

    form=AgregarIndTerapeuticaForm()
    info = {'form':form,'indicaciones':indicaciones,'emergencia':emer,'triage':triage}
    return render_to_response('atencion_indT.html',info,context_instance=RequestContext(request))

#------------------------------Gestion de Indicaciones Diagnosticas- Generico
@login_required(login_url='/')
def emergencia_indicacionesD(request,id_emergencia):
    
    # FUNCION PARA MANIPULAR EL FORMULARIO Y PARA LISTAR LAS INDICACIONES Diagnosticas
    # Consultas para guardar abajo los objetos pertinentes
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    #usr = Usuario.objects.get(username=request.user)
    #print "usuario es:",usr
    ingreso = datetime.now()
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    #categoria = 0
    #indicaciones = Indicacion.objects.filter()
    indicaciones = Indicacion.objects.filter(asignar__emergencia = id_emergencia)
    print "indicaciones: ",indicaciones
    
    ###Codigo Form:
    mensaje = ""
    if request.method == 'POST':
        form = AgregarIDLabForm(request.POST)
        print "Validez Formulario:",str(form.is_valid())
        #Print de inputs del formulario
        print "veo tipo:",form.cleaned_data['nombreDL']
        print "veo nombre:",form.cleaned_data['otroDL']
        if form.is_valid():
            pcd = form.cleaned_data
            p_nombre            = pcd['nombreDL']
            p_otro              = pcd['otroDL']
            #Agrego indicacion dependiendo del tipo
            print "veo nombre:",p_nombre
            print "veo otro:",p_otro
            
            indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = p_nombre)
            #print "indicaciones: ",len(indicaciones)
            if indicacionesQ:
                # Falta agregar Condicional cuando tengo indicaciones de tipo terapeutico q no tienen categoria
                mensaje = "Hay indicaciones con ese nombre"
                #OJO AQUI TENGO QUE PASARLE LA TABLA DE ASIGNAR para que pueda listar la hora
                info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones}
                return render_to_response('atencion_indD.html',info,context_instance=RequestContext(request))
            else:
                print "no hay elementos"
                #Agrego para ver si sirve
                print "Input p_tipo",p_nombre
                print "Input p_nombre",p_otro
                i = Indicacion(nombre=p_nombre,tipo="terapeutico")
                i.save()
                a = Asignar(emergencia=emer,indicacion=i,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                a.save()
                mensaje = "Guardado Exitosamente"
                
                #OJO AQUI TENGO QUE PASARLE LA TABLA DE ASIGNAR para que pueda listar la hora
                info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones}
                return render_to_response('atencion_indD.html',info,context_instance=RequestContext(request))

    form = AgregarIDLabForm(request.POST)
    info = {'form':form,'indicaciones':indicaciones,'emergencia':emer,'triage':triage}
    return render_to_response('atencion_indD.html',info,context_instance=RequestContext(request))


#---------------------------------------------Gestion de Diagnostico Definitivo
@login_required(login_url='/')
def emergencia_diagnostico(request,id_emergencia):
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    ###Codigo Form:
    mensaje = ""
    if request.method == 'POST':
        form = AgregarDiagnosticoForm(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            p_diagnostico = pcd['diagnostico']
            p_comentario  = pcd['comentario']
    form = AgregarDiagnosticoForm()
    info = {'form':form,'emergencia':emer,'triage':triage}
    return render_to_response('atencion_diag.html',info,context_instance=RequestContext(request))
            

########################################################HASTA AQUI CODIGO ATENCION

@login_required(login_url='/')
def emergencia_egreso(request,id_emergencia):
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    ###Codigo Form:
    mensaje = ""
    if request.method == 'POST':
        form = AgregarEgresoForm(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            p_destino          = pcd['destino']
            p_area_admision    = pcd['area_admision']
            p_fecha_traslado   = pcd['fecha_traslado']
            p_fecha_indicacion = pcd['fecha_indicacion']
    form = AgregarEgresoForm()
    info = {'form':form,'emergencia':emer,'triage':triage}
    return render_to_response('atencion_egre.html',info,context_instance=RequestContext(request))
            
