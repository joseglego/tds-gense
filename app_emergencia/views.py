# -*- encoding: utf-8 -*-
# coding: latin1

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
from django.utils.timezone import utc
from datetime import datetime, date, timedelta
from models import *
from forms import *
from app_usuario.forms import *

# Estadisticas
from django.db.models import Count

#####################################################
#Imports Atencion
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from app_enfermedad.models import *
######################################################

def emergencia_buscar(request):
    mensaje = ""
    titulo = "Busqueda de Pacientes"
    boton = "Buscar"
    info = {}
    form = IniciarSesionForm()
    if request.method == 'POST':
        busqueda = BuscarEmergenciaForm(request.POST)
        resultados = []
        if busqueda.is_valid():
            pcd = busqueda.cleaned_data
            p_cedula = pcd['cedula']
            p_nombres = pcd['nombres']
            p_apellidos = pcd['apellidos']

            if len(p_cedula) > 0:
                print "Se busco por cedula"
                print p_cedula
                pacientes = Paciente.objects.filter(cedula__startswith=p_cedula)
                if len(pacientes) > 0:
                    for p in pacientes:
                        resultados.append(p)
            else:
                print "Se busco por NO cedula"
                print "nombres:"+p_nombres+"y apellidos "+p_apellidos
                if len(p_nombres) > 0 and len(p_apellidos) > 0:
                    print "Se busco por Nombre y Apellido"
                    pacientes = Paciente.objects.filter(nombres__icontains=p_nombres,apellidos__icontains=p_apellidos)
                    if len(pacientes) > 0:
                        for p in pacientes:
                            resultados.append(p)
                elif len(p_apellidos) == 0:
                    print "Se busco por Nombre"
                    pacientes = Paciente.objects.filter(nombres__icontains=p_nombres)
                    if pacientes:
                        for p in pacientes:
                            resultados.append(p)
                elif len(p_nombres) == 0:
                    print "Se busco por Apellido"
                    pacientes = Paciente.objects.filter(apellidos__icontains=p_apellidos)
                    if pacientes:
                        for p in pacientes:
                            resultados.append(p)
            lista = []
            for p in resultados:
                emergencias = Emergencia.objects.filter(paciente=p)
                for e in emergencias:
                    lista.append(e)
                    
        info = {'form':form,'lista':lista,'titulo':titulo}
        return render_to_response('lista.html',info,context_instance=RequestContext(request))
    else:
        busqueda = BuscarEmergenciaForm()
    
    info = {'form':form,'busqueda':busqueda,'titulo':titulo,'boton':boton}
    return render_to_response('busqueda.html',info,context_instance=RequestContext(request))

def emergencia_listar_todas(request):   
    lista = Emergencia.objects.filter(hora_egreso=None)
    form = IniciarSesionForm()
    titulo = "Área de Emergencias"
    info = {'lista':lista,'form':form,'titulo':titulo}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_triage(request):
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.atendido() == False]
    form = IniciarSesionForm()
    titulo = "Área de Triage"
    info = {'lista':lista,'form':form,'titulo':titulo}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_sinclasificar(request):    
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.triage() == 0]
    form = IniciarSesionForm()
    titulo = "Sin Clasificar"
    info = {'lista':lista,'form':form,'titulo':titulo}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_clasificados(request):    
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.triage() != 0 and i.atendido() == False]
    form = IniciarSesionForm()
    titulo = "Clasificados"
    info = {'lista':lista,'form':form,'titulo':titulo}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

def emergencia_listar_atencion(request):
    lista = Emergencia.objects.filter(hora_egreso=None)
    lista = [i for i in lista if i.atendido() == True]
    form = IniciarSesionForm()
    titulo = "Área de Atención"
    info = {'lista':lista,'form':form,'titulo':titulo}
    return render_to_response('lista.html',info,context_instance=RequestContext(request))

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
            recursos = 2
            if (vTriage == 1):
                atencion = True
            elif (vTriage == 2):
                atencion = False
                esperar = False
            else:
                if (vTriage == 4):
                    recursos = 1
                elif (vTriage == 5):
                    recursos = 0
                atencion = False
                esperar = True
            t = Triage(emergencia = emergencia,medico=medico,fecha=fechaReal,motivo=motivo,atencion=atencion,esperar=esperar,areaAtencion=area,recursos=recursos,nivel=vTriage)
            t.save()
            return redirect("/paciente/"+str(emergencia.paciente.id))
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
            f_ingreso  = pcd['ingreso']
            f_temp     = pcd['signos_tmp']
            f_fc       = pcd['signos_fc']
            f_fr       = pcd['signos_fr']
            f_pa       = pcd['signos_pa']
            f_pb       = pcd['signos_pb']
            f_saod     = pcd['signos_saod']
            f_avpu     = pcd['signos_avpu']

            f_dolor    = pcd['signos_dolor']
            f_atencion = False
            f_esperar = True
            f_recursos = 2

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
            return redirect("/paciente/"+str(emergencia.paciente.id))
        else:
            print "Error 2"
    form = calcularTriageForm()
    info = {'form':form,'idE':idE}
    return render_to_response('calcularTriage.html',info,context_instance=RequestContext(request))

def estadisticas_prueba():
#    triages = Triage.objects.filter(fecha__year=ano).filter(fecha__month=mes).values('nivel').annotate(Count('nivel')).order_by('nivel')
#    triages = [[i['nivel'],i['nivel__count']] for i in triages]
#    triagesBien = [[1,0],[2,0],[3,0],[4,0],[5,0]]
#    for i in triages:
#      triagesBien[i['nivel']] = i['count']
    triages = Triage.objects.all().values('nivel').annotate(Count('nivel')).order_by('nivel')
    triages = [[i['nivel'],i['nivel__count']] for i in triages]
    triagesBien = [0,0,0,0,0]
    for i in triages:
        triagesBien[i[0]-1] = i[1]
    triages = []
    for i in range(5):
      triages.append([(i+1),triagesBien[i]])
    return triages

def estadisticas_sem(request,anho,mes,dia):
    # Datos generales
    fecha = date(int(anho),int(mes),int(dia))
    ini_sem = fecha - timedelta(days=7)
    sig_sem = fecha + timedelta(days=7)
    fin_sem = fecha - timedelta(days=1)

    ingresos = Emergencia.objects.filter(hora_ingreso__range=[ini_sem,fecha])
    es = Emergencia.objects.filter(hora_egreso__range=[ini_sem,fecha])
    
    # Cuanto se tardo cada emergencia
    horas0a2=0
    horas2a4=0
    horas4a6=0
    horas6aM=0
    hora = 3600
    for e in es:
        t = e.tiempo_emergencia() 
        if t < 2*hora:
            horas0a2 += 1
        elif t >= 2*hora and t < 4*hora:
            horas2a4 += 1
        elif t >= 4*hora and t < 6*hora:
            horas4a6 += 1
        else:
            horas6aM += 1
    total = horas0a2 + horas2a4 + horas4a6 + horas6aM
    
    # Resultados de los Triages
    triages = Triage.objects.filter(fecha__range=[ini_sem,fin_sem]).values('nivel').annotate(Count('nivel')).order_by('nivel')
    triages = [[i['nivel'],i['nivel__count']] for i in triages]
    triagesBien = [0,0,0,0,0]
    for i in triages:
        triagesBien[i[0]-1] = i[1]
    triages = []
    for i in range(5):
      triages.append([(i+1),triagesBien[i]])
    egresos = [['Total',total],['Menos de 2 horas',horas0a2],['2 a 4 horas',horas2a4],['4 a 6 horas',horas4a6],['Más de 6 horas',horas6aM]]
    info = {'triages':triages,'fecha':fecha,'inicio':ini_sem,'fin':fin_sem,'sig':sig_sem,'total_ingresos':len(ingresos),'total_egresos':total,'egresos':egresos}
    return render_to_response('estadisticas.html',info,context_instance=RequestContext(request))

def estadisticas(request):
    hoy = datetime.today()
    return redirect('/estadisticas/dia/'+str(hoy.year)+'-'+str(hoy.month)+'-'+str(hoy.day))

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
    pdf    = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

def emergencia_descarga(request,id_emergencia):
    emer  = get_object_or_404(Emergencia,id=id_emergencia)
    #triages = Triage.objects.filter(emergencia=self.id).order_by("-fechaReal")
    #ctx = {'emergencia':emer,'triage':triage}
    # TERMINAR CONSULTAS PARA INGRESAR AL CONTEXTO
    ctx  = {'emergencia':emer}
    html = render_to_string('historia_med.html',ctx, context_instance=RequestContext(request))
    return generar_pdf(html)

#----------------------------------Gestion de Enfermedad Actual
@login_required(login_url='/')
def emergencia_enfermedad_actual(request,id_emergencia):
    emer = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    mensaje = ""
    atList = Atencion.objects.filter(emergencia=id_emergencia)
    
    if len(atList) == 0:
        atencion = Atencion(emergencia=emer,medico=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now(),area_atencion=triage.areaAtencion)
        atencion.save()
    if request.method == 'POST':
        form = AgregarEnfActual(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            narrativa          = pcd['narrativa']
            # Busco si ya existe una narrativa para esa indicacion
            # enfA = EnfermedadActual.objects.get(atencion=atencion.id)
            ## Si existe, la sobreescribo
            # if enfA:
            #     enfA.update(narrativa=narrativa)
            # else:
            #     enfA = EnfermedadActual(atencion=atencion,narrativa=narrativa)
            #     enfA.save()
            # mensaje = " Agregado exitosamente"
            # info = {'form':form,'emergencia':emer,'triage':triage, 'mensaje':mensaje}
            # return render_to_response('atencion_enfA.html',info,context_instance=RequestContext(request))

            enfA = EnfermedadActual(atencion=atList[0],narrativa=narrativa)
            enfA.save()
            mensaje = "Narrativa Agregada Exitosamente: "+enfA.narrativa
            info = {'form':form,'emergencia':emer,'triage':triage, 'mensaje':mensaje}
            return render_to_response('atencion_enfA.html',info,context_instance=RequestContext(request))

    form = AgregarEnfActual()
    info = {'form':form,'emergencia':emer,'triage':triage, 'mensaje':mensaje}
    return render_to_response('atencion_enfA.html',info,context_instance=RequestContext(request))

# --- RGV

@login_required(login_url='/')
def emergencia_atencion(request,id_emergencia):
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    ctx    = {'emergencia':emer,'triage':triage}
    return render_to_response('atencion.html',ctx,context_instance=RequestContext(request))

def emergencia_antecedentes_agregar(request,id_emergencia,tipo_ant):
    emer    = get_object_or_404(Emergencia,id=id_emergencia)
    paci    = Paciente.objects.get(emergencia__id=id_emergencia)
    triage  = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage  = triage[0]
    if request.method == 'POST':
        nombres  = request.POST.getlist('nuevoNombre')
        fechas   = request.POST.getlist('nuevoFecha')
        atributo = request.POST.getlist('nuevoAtributo3')
        for i in range(len(nombres)-1): 
            ant       = Antecedente(tipo=tipo_ant,nombre=nombres[i])
            ant.save()
            pertenece = Pertenencia(paciente=paci,antecedente=ant)
            pertenece.save()
            if tipo_ant =='medica' or tipo_ant =='quirurgica':
                fecha = Fecha(fecha=fechas[i],pertenencia=pertenece) 
                fecha.save()
                if tipo_ant == 'medica':
                    tratamiento = Tratamiento(nombre=atributo[i])
                    tratamiento.save()
                    trataPerte  = TratamientoPertenencia(pertenencia=pertenece,tratamiento=tratamiento)
                    trataPerte.save() 
                if tipo_ant == 'quirurgica':
                    lugar      = Lugar(nombre=atributo[i])
                    lugar.save()
                    lugarperte = LugarPertenencia(lugar=lugar,pertenencia=pertenece)
                    lugarperte.save()
    pertenece = Pertenencia.objects.filter(paciente=paci,antecedente__tipo=tipo_ant)
    ctx = {'emergencia':emer,'triage':triage,'pertenece':pertenece,'tipo_ant':tipo_ant}
    return render_to_response('atencion_ant_medica.html',ctx,context_instance=RequestContext(request))


def emergencia_antecedentes_modificar(request,id_emergencia,tipo_ant):
    emer         = get_object_or_404(Emergencia,id=id_emergencia)
    paci         = Paciente.objects.get(emergencia__id=id_emergencia)
    triage       = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage       = triage[0]
    antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci,tipo=tipo_ant)
    for ant in antecedentes:
        ant.nombre = request.POST[str(ant.id)+"nombre"]
        if tipo_ant == 'medica' or tipo_ant == 'quirurgica':
            pertenece = Pertenencia.objects.filter(paciente=paci,antecedente=ant)
            if pertenece:
                fecha             = Fecha.objects.get(pertenencia=pertenece[0])
                fecha.fecha       = request.POST[str(ant.id)+"fecha"]
                fecha.pertenencia = pertenece[0]
                fecha.save()
            if tipo_ant == 'medica':
                tratamiento = Tratamiento.objects.filter(tratamientopertenencia__pertenencia=pertenece[0])
                if tratamiento:
                    tratamiento[0].nombre = request.POST[str(ant.id)+"atributo3"]
                    tratamiento[0].save()
            if tipo_ant == 'quirurgica':
                lugar = Lugar.objects.filter(lugarpertenencia__pertenencia=pertenece[0])
                if lugar:
                    lugar[0].nombre = request.POST[str(ant.id)+"atributo3"]
                    lugar[0].save()
        ant.save()
    pertenece = Pertenencia.objects.filter(paciente=paci,antecedente__tipo=tipo_ant)
    ctx = {'emergencia':emer,'triage':triage,'pertenece':pertenece,'tipo_ant':tipo_ant}
    return render_to_response('atencion_ant_medica.html',ctx,context_instance=RequestContext(request))

def emergencia_antecedentes_eliminar(request,id_emergencia,tipo_ant):
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    paci   = Paciente.objects.get(emergencia__id=id_emergencia)
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci,tipo=tipo_ant)
    if request.method == 'POST':
        checkes = request.POST.getlist(u'check')
        for id_ant in checkes:
            ant       = Antecedente(id=id_ant)
            pertenece = Pertenencia.objects.filter(paciente=paci,antecedente_id=id_ant)
            if pertenece:
                fecha  = Fecha.objects.filter(pertenencia=pertenece[0])
                fecha.delete()
                lugarpertence = LugarPertenencia.objects.filter(pertenencia=pertenece[0])
                if lugarpertence:
                    lugarpertence.delete()
                tratamiento = TratamientoPertenencia.objects.filter(pertenencia=pertenece[0])
                if tratamiento:
                    tratamiento.delete() 
            pertenece.delete()
    pertenece = Pertenencia.objects.filter(paciente=paci,antecedente__tipo=tipo_ant)
    ctx = {'emergencia':emer,'triage':triage,'pertenece':pertenece,'tipo_ant':tipo_ant}
    return render_to_response('atencion_ant_medica.html',ctx,context_instance=RequestContext(request))


#----------------------------------Gestion de Antecedentes en area de Atencion
@login_required(login_url='/')
def emergencia_antecedentes(request,id_emergencia):
    emer   = get_object_or_404(Emergencia,id=id_emergencia)
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    ctx    = {'emergencia':emer,'triage':triage}
    return render_to_response('atencion_ant.html',ctx,context_instance=RequestContext(request))

#----------------------------------Gestion de Antecedentes en area de Atencion
@login_required(login_url='/')
def emergencia_antecedentes_tipo(request,id_emergencia,tipo_ant):
    emer         = get_object_or_404(Emergencia,id=id_emergencia)
    paci         = Paciente.objects.get(emergencia__id=id_emergencia)
    triage       = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage       = triage[0]
    pertenece    = Pertenencia.objects.filter(paciente=paci,antecedente__tipo=tipo_ant)
    antecedentes = Antecedente.objects.filter(pertenencia__paciente=paci,tipo=tipo_ant)
    ctx = {'emergencia':emer,'triage':triage,'antecedentes':antecedentes,'pertenece':pertenece,'tipo_ant':tipo_ant}
    return render_to_response('atencion_ant_medica.html',ctx,context_instance=RequestContext(request))


#--------------------------------Gestion de Enfermedad (Examen Fisico)
@login_required(login_url='/')
def emergencia_enfermedad(request,id_emergencia):
    emer        = get_object_or_404(Emergencia,id=id_emergencia)
    paci        = Paciente.objects.get(emergencia__id=id_emergencia)
    triage      = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage      = triage[0]
    causa       = 0
    atencion    = Atencion.objects.filter(emergencia=id_emergencia)
    aspectos    = Aspecto.objects.filter(parteaspecto__partecuerpo__nombre='CABEZA Y ROSTRO')
    aspectoAten = AspectoAtencion.objects.filter(atencion=atencion[0],aspecto__parteaspecto__partecuerpo__nombre='CABEZA Y ROSTRO')
    ctx = {'emergencia':emer,'triage':triage,'causa':causa}
    if paci.sexo == 1:
        return render_to_response('atencion_Plan.html',ctx,context_instance=RequestContext(request))
    else:
        return render_to_response('atencion_Plan_mujer.html',ctx,context_instance=RequestContext(request))

@login_required(login_url='/')
def emergencia_enfermedad_zonacuerpo(request,id_emergencia,zona_cuerpo):
    emer         = get_object_or_404(Emergencia,id=id_emergencia)
    paci         = Paciente.objects.get(emergencia__id=id_emergencia)
    triage       = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage       = triage[0]
    causa        = 0
    atencion     = Atencion.objects.filter(emergencia=id_emergencia)
    partecuerpo  = ParteCuerpo.objects.filter(zonaparte__zonacuerpo__nombre=zona_cuerpo)
    parteaspecto = ParteAspecto.objects.filter(partecuerpo__zonaparte__zonacuerpo__nombre=zona_cuerpo)
    aspectoAten  = AspectoAtencion.objects.filter(atencion=atencion[0],aspecto__parteaspecto__partecuerpo__zonaparte__zonacuerpo__nombre=zona_cuerpo)
    aspectos     = Aspecto.objects.filter(parteaspecto__partecuerpo__zonaparte__zonacuerpo__nombre=zona_cuerpo)
    ctx = {'emergencia':emer,'triage':triage,'causa':causa,'paciente':paci,'partecuerpo':partecuerpo,'parteaspecto':parteaspecto,'aspectoAtencion':aspectoAten,'zona_cuerpo':zona_cuerpo}
    return render_to_response('atencion_Plan_cuerpo.html',ctx,context_instance=RequestContext(request))

@login_required(login_url='/')
def emergencia_enfermedad_partecuerpo(request,id_emergencia,parte_cuerpo):
    emer        = get_object_or_404(Emergencia,id=id_emergencia)
    triage      = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage      = triage[0]
    causa       = 0
    atencion    = Atencion.objects.filter(emergencia=id_emergencia)
    atencion    = atencion[0]
    aspectoAten = AspectoAtencion.objects.filter(atencion=atencion,aspecto__parteaspecto__partecuerpo__nombre=parte_cuerpo)
    aspectos    = Aspecto.objects.filter(parteaspecto__partecuerpo__nombre=parte_cuerpo)
    if not(aspectoAten):
        for aspe in aspectos:
            AspeAten = AspectoAtencion(revisado='no',aspecto=aspe,atencion=atencion)
            AspeAten.save()
    aspectoAten = AspectoAtencion.objects.filter(atencion=atencion,aspecto__parteaspecto__partecuerpo__nombre=parte_cuerpo)
    ctx = {'emergencia':emer,'triage':triage,'causa':causa,'aspectoAtencion':aspectoAten,'parte_cuerpo':parte_cuerpo}
    return render_to_response('atencion_Plan_partecuerpo.html',ctx,context_instance=RequestContext(request))

@login_required(login_url='/')
def emergencia_enfermedad_enviarcuerpo(request,id_emergencia,parte_cuerpo):
    emer        = get_object_or_404(Emergencia,id=id_emergencia)
    triage      = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage      = triage[0]
    causa       = 0
    atencion    = Atencion.objects.filter(emergencia=id_emergencia)
    atencion    = atencion[0]
    aspectoAten = AspectoAtencion.objects.filter(atencion=atencion,aspecto__parteaspecto__partecuerpo__nombre=parte_cuerpo)
    partecuerpo = 0
    for aspAten in aspectoAten:
        input1 = request.POST[str(aspAten.aspecto.id)]
        if input1 == 'normal':
            aspAten.revisado = '1'
            anomalia = Anomalia.objects.filter(aspectoatencion=aspAten)
            if anomalia:
                anomalia.delete()
            aspAten.save()
        elif input1 == 'anormal':
            aspAten.revisado = '1'
            anomalia         = Anomalia.objects.filter(aspectoatencion=aspAten)
            descripcion      = request.POST['A'+str(aspAten.aspecto.id)]
            if anomalia:
                anomalia.descripcion = descripcion 
                anomalia.save() 
            else:
                anomalia = Anomalia(descripcion=descripcion,aspectoatencion=aspAten)
                anomalia.save()
            aspAten.save()
        elif input1 == 'no':
            aspAten.revisado = '0'
            anomalia         = Anomalia.objects.filter(aspectoatencion=aspAten)
            if anomalia:
                anomalia.delete()
            aspAten.save()
        
    return HttpResponse()
# --- RGV

#----------------------------------------------------------Gestion de INDICACIONES
@login_required(login_url='/')
def emergencia_indicaciones_ini(request,id_emergencia):
    emer = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    ingreso = datetime.now()
    indicaciones = Indicacion.objects.filter(asignar__emergencia = id_emergencia)
    info = {'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'ingreso':ingreso}
    return render_to_response('atencion_ind.html',info,context_instance=RequestContext(request))

#Agrega las indicaciones dependiendo de la categoria: 
@login_required(login_url='/')
def emergencia_indicaciones(request,id_emergencia,tipo_ind):
    emer = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    ingreso = datetime.now()
    mensaje=""

    #------------------ Gestion de indicaciones con interfaz de tabla----------------------#
    if tipo_ind == 'listar':
        indicaciones = Asignar.objects.filter(emergencia = id_emergencia)
        info = {'mensaje':mensaje, 'emergencia':emer,'triage':triage,'indicaciones':indicaciones}
        return render_to_response('atencion_ind_listar.html',info,context_instance=RequestContext(request))

    elif tipo_ind == 'medicamento':
        indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
        info = {'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'tipo_ind':tipo_ind}
        return render_to_response('atencion_ind_medica.html',info,context_instance=RequestContext(request))

    elif tipo_ind == 'valora' or tipo_ind == 'otros' or tipo_ind == 'terapeutico':
        indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
        info = {'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'tipo_ind':tipo_ind}
        return render_to_response('atencion_ind_tera.html',info,context_instance=RequestContext(request))
    
    #------------ Gestion de indicaciones con interfaz de forms de Django-------------------#
    else:
        indicaciones = Indicacion.objects.filter(tipo__iexact=tipo_ind)
        if request.method == 'POST':
            if tipo_ind == 'dieta':
                form = AgregarIndDietaForm(request.POST)
                
            elif tipo_ind == 'hidrata':
                form = AgregarIndHidrataForm(request.POST)

            elif tipo_ind == 'lab':
                form = AgregarIndLabForm(request.POST)

            elif tipo_ind == 'imagen':
                form = AgregarIndImgForm(request.POST)

            elif tipo_ind == 'endoscopico':
                form = AgregarIndEndosForm(request.POST)
    
            if form.is_valid():
                pcd = form.cleaned_data
                nombre = pcd[tipo_ind]
                print "IMprime lo que me retorna el form %s: "% (tipo_ind),nombre
                
                # Condicional para validar/agregar indicaciones de tipo lab/endoscopicos:
                if tipo_ind == 'lab' or tipo_ind == 'endoscopico':
                    for i in range(len(nombre)):
                        indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = nombre[i])
                        
                        if indicacionesQ:
                            mensaje = "Hay indicaciones con este nombre: "+ indicacionesQ[0].nombre
                            info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'ingreso':ingreso, 'tipo_ind':tipo_ind}
                            return render_to_response('atencion_ind_hidrata.html',info,context_instance=RequestContext(request))
                        
                        else:
                            indicaciones = Asignar.objects.filter(emergencia = id_emergencia)
                            i= Indicacion.objects.get(nombre = nombre[i])
                            a = Asignar(emergencia=emer,indicacion=i,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                            a.save()

                    mensaje = "Procedimientos Guardado Exitosamente"
                    info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
                    return render_to_response('atencion_ind_listar.html',info,context_instance=RequestContext(request))

                if tipo_ind == 'imagen':
                    for i in range(len(nombre)):
                        indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = nombre[i])
                        if indicacionesQ:
                            mensaje = "Hay indicaciones con este nombre: "+indicacionesQ[0].nombre
                            info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'ingreso':ingreso, 'tipo_ind':tipo_ind}
                            return render_to_response('atencion_ind_hidrata.html',info,context_instance=RequestContext(request))
                        
                        else:
                            indicaciones = Asignar.objects.filter(emergencia = id_emergencia)
                            i= Indicacion.objects.get(nombre = nombre[i])
                            a = Asignar(emergencia=emer,indicacion=i,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                            a.save()
                            p_cuerpo = request.POST["c_"+str(i.id)]
                            ex = EspImg(asignacion=a,parte_cuerpo=p_cuerpo)
                            ex.save()

                    mensaje = "Procedimientos Guardado Exitosamente"
                    info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
                    return render_to_response('atencion_ind_listar.html',info,context_instance=RequestContext(request))

                # Condicional para validar/agregar indicaciones de tipo dieta e hidratacion
                else:
                    indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = nombre)
                    if indicacionesQ:
                        mensaje = "Hay indicaciones con este nombre: "+indicacionesQ[0].nombre
                        info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'ingreso':ingreso, 'tipo_ind':tipo_ind}
                        return render_to_response('atencion_ind_hidrata.html',info,context_instance=RequestContext(request))
                    else:
                        indicaciones = Asignar.objects.filter(emergencia = id_emergencia)
                        i= Indicacion.objects.get(nombre = nombre)
                        a = Asignar(emergencia=emer,indicacion=i,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                        a.save()
                        if tipo_ind == 'dieta':
                            extra = pcd['observacion']
                            ex = EspDieta(asignacion=a,observacion=extra)
                            ex.save()
                        elif tipo_ind == 'hidrata':
                            sn = pcd['combina']
                            vol    = pcd['volumen']
                            vel    = pcd['vel_inf']
                            comp   = pcd['complementos']
                            ex = EspHidrata(asignacion=a,volumen=vol,vel_infusion=vel,complementos=comp)
                            ex.save()
                            if pcd['combina'] == "True":
                                ex_sol = pcd ['combina_sol']
                                i2= Indicacion.objects.get(nombre = ex_sol)
                                comb = CombinarHidrata(hidratacion1= ex,hidratacion2=i2)
                                comb.save()
                        mensaje = "Procedimientos Guardado Exitosamente"
                        info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
                        return render_to_response('atencion_ind_listar.html',info,context_instance=RequestContext(request))

            else:
                form_errors = form.errors
                info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'ingreso':ingreso, 'tipo_ind':tipo_ind,'form_errors': form_errors}
                return render_to_response('atencion_ind_hidrata.html',info,context_instance=RequestContext(request))

        #---------Renderizado de formularios al ingresar por primera vez-----#
        if tipo_ind == 'dieta':
            form=AgregarIndDietaForm()

        elif tipo_ind == 'hidrata':
            form = AgregarIndHidrataForm()

        elif tipo_ind == 'lab':
            form = AgregarIndLabForm()

        elif tipo_ind == 'imagen':
            form = AgregarIndImgForm()

        elif tipo_ind == 'endoscopico':
            form = AgregarIndEndosForm()

        info = {'form':form,'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'ingreso':ingreso, 'tipo_ind':tipo_ind}
        return render_to_response('atencion_ind_hidrata.html',info,context_instance=RequestContext(request))

#-----------------------------------------------Acciones CRUD
#--------------------------------------------AGREGAR
@login_required(login_url='/')
def emergencia_indicaciones_agregar(request,id_emergencia,tipo_ind):
    emer = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    mensaje = ""
    atencion = Atencion.objects.filter(emergencia= emer)
    diags = EstablecerDiag.objects.filter(atencion=atencion[0])
    
    if request.method == 'POST':
        if tipo_ind == 'diagnostico':
            diagnostico  = request.POST.getlist('nuevoDiag')
            #Consulta diagnosticos:
            ver = range(len(diagnostico)-1)
            for i in ver:
                # Condicional para saber si existen los diagnosticos:
                diagnosticoQ = Diagnostico.objects.filter(establecerdiag__atencion = atencion[0],establecerdiag__diagnostico__nombreD = diagnostico[i])
                if diagnosticoQ:
                    mensaje = "Hay Diagnosticos con este nombre: "+diagnosticoQ[0].nombreD
                    info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'tipo_ind':tipo_ind,'diags':diags}
                    return render_to_response('atencion_diag.html',info,context_instance=RequestContext(request))
                else:
                    diag = Diagnostico.objects.filter(nombreD__iexact=diagnostico[i])
                    # Si ya existe ese diagnostico creado, busco su id y lo asigno
                    if len(diag) == 0:
                        diag = Diagnostico(nombreD=diagnostico[i])
                        diag.save()
                        est_Diag = EstablecerDiag(atencion=atencion[0],diagnostico=diag,fecha=datetime.now(),fechaReal=datetime.now())
                        est_Diag.save()
                    else:
                        est_Diag = EstablecerDiag(atencion=atencion[0],diagnostico=diag[0],fecha=datetime.now(),fechaReal=datetime.now())
                        est_Diag.save()
                    
            mensaje = "Diagnosticos guardados Exitosamente"
            info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'tipo_ind':tipo_ind,'diags':diags}
            return render_to_response('atencion_diag.html',info,context_instance=RequestContext(request))

        elif tipo_ind == 'valora' or tipo_ind == 'otros' or tipo_ind == 'terapeutico':
            indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
            nombres         = request.POST.getlist('nuevaInd')
            ver = range(len(nombres)-1)
            for i in ver:
                # Condicional para saber si existe en las indicaciones:
                indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = nombres[i])
                if indicacionesQ:
                    mensaje = "Hay indicaciones con este nombre: "+indicacionesQ[0].nombre
                    info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
                    return render_to_response('atencion_ind_tera.html',info,context_instance=RequestContext(request))
                else:
                    #Creo el objeto indicacion
                    ind = Indicacion(nombre=nombres[i],tipo=tipo_ind)
                    ind.save()
                    a = Asignar(emergencia=emer,indicacion=ind,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                    a.save()
            mensaje = "Indicaciones guardadas Exitosamente"
            info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
            return render_to_response('atencion_ind_tera.html',info,context_instance=RequestContext(request))

        elif tipo_ind == 'medicamento':
            indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
            nombres         = request.POST.getlist('nuevaMed')
            dosis           = request.POST.getlist('nuevaDosis')
            tc              = request.POST.getlist('nuevoTC')
            frec            = request.POST.getlist('nuevaFrec')
            via             = request.POST.getlist('nuevaVAD')
            tf              = request.POST.getlist('nuevoTF')
            situacion       = request.POST.getlist('situacion')
            comentario      = request.POST.getlist('comentario')
            ver = range(len(nombres)-1)
            
            for i in ver:
                # Condicional para saber si existe en las indicaciones:
                indicacionesQ = Indicacion.objects.filter(asignar__emergencia = id_emergencia,asignar__indicacion__nombre = nombres[i])
                if indicacionesQ:
                    mensaje = "Hay indicaciones con este nombre: "+indicacionesQ[0].nombre
                    info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
                    return render_to_response('atencion_ind_medica.html',info,context_instance=RequestContext(request))
                else:
                    #Creo el objeto indicacion
                    ind = Indicacion(nombre=nombres[i],tipo=tipo_ind)
                    ind.save()
                    a = Asignar(emergencia=emer,indicacion=ind,persona=emer.responsable,fecha=datetime.now(),fechaReal=datetime.now())
                    a.save()
                    # Agregar info extra:
                    eMed= EspMedics(asignacion=a,dosis=float(dosis[i]),tipo_conc =tc[i],frecuencia=frec[i],tipo_frec=tf[i],via_admin=via[i])
                    eMed.save()
                    if tf[i] =="sos":
                        print "situaciones = ", situacion
                        print "comentarios = ", comentario
                        tSos= tieneSOS(espMed=eMed,situacion=situacion[i],comentario=comentario[i])
                        tSos.save()
                    
            mensaje = "Medicaciones guardadas Exitosamente"
            info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
            return render_to_response('atencion_ind_medica.html',info,context_instance=RequestContext(request))
    else:
        mensaje = "ELSE PORQ NO HAY POST"
        info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'indicaciones':indicaciones,'tipo_ind':tipo_ind}
        return render_to_response('atencion_ind_medica.html',info,context_instance=RequestContext(request))


#--------------------------------------------ELIMINAR
@login_required(login_url='/')
def emergencia_indicaciones_eliminar(request,id_emergencia,tipo_ind):
    emer = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    mensaje = ""
    atencion = Atencion.objects.filter(emergencia= emer)
    
    if request.method == 'POST':
        checkes = request.POST.getlist(u'check')
        if tipo_ind == "diagnostico":
            # obj tiene el id de la relacion
            for obj in checkes:
                relDiag = EstablecerDiag.objects.get(id=obj)
                # Borro ese objeto:
                relDiag.delete()
                diags = EstablecerDiag.objects.filter(atencion=atencion[0])
            mensaje = "Diagnosticos eliminado Exitosamente"
            info = {'mensaje':mensaje,'emergencia':emer,'triage':triage,'tipo_ind':tipo_ind,'diags':diags}
            return render_to_response('atencion_diag.html',info,context_instance=RequestContext(request))

        elif tipo_ind == 'valora' or tipo_ind == 'otros' or tipo_ind == 'terapeutico':
            for obj in checkes:
                asig = Asignar.objects.get(id=obj)
                ind  = Indicacion.objects.filter(nombre=asig.indicacion.nombre) 
                ind[0].delete()
                asig.delete()
            indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
            mensaje = "Indicacion Eliminada Exitosamente"
            info = {'mensaje':mensaje, 'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'tipo_ind':tipo_ind}
            return render_to_response('atencion_ind_tera.html',info,context_instance=RequestContext(request))

        elif tipo_ind == "medicamento":
            for obj in checkes:
                asig = Asignar.objects.get(id=obj)
                print "objeto asignar a eliminar:",asig
                # Busco la info extra y la borro:
                extra  = EspMedics.objects.get(asignacion=asig)
                pastilla = Indicacion.objects.filter(nombre=asig.indicacion.nombre)
                pastilla[0].delete()
                extra.delete()
                asig.delete()
                
            indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
            mensaje = "Medicamento Eliminado Exitosamente"
            info = {'mensaje':mensaje, 'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'tipo_ind':tipo_ind}
            return render_to_response('atencion_ind_medica.html',info,context_instance=RequestContext(request))

#--------------------------------------------MODIFICAR
# def emergencia_indicaciones_modificar(request,id_emergencia,tipo_ind):
#     emer   = get_object_or_404(Emergencia,id=id_emergencia)
#     paci = Paciente.objects.filter(emergencia__id=id_emergencia)
#     paci = paci[0]
#     triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
#     triage = triage[0]
#     mensaje = ""

#     if tipo_ind =="diagnostico":

#     elif tipo_ind =="medicamento":
#         # Version 1 Sin POST:
#         indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
#         print "Medicamentos asignados para esa emergencia:",indicaciones
#         for ind in indicaciones:
#             ind.indicacion.nombre = request.POST[str(ind.id)+"nombre"]
#             print "Lo que tengo en el input:",ind.indicacion.nombre
#             print "Veo id de indicacion en asignar:",ind.indicacion.id
#             ii= Indicacion.objects.get(id = ind.indicacion.id)
#             ii.nombre = request.POST[str(ind.id)+"nombre"]
#             ii.save()
#             print "Veo id de indicacion elegida:",ii.id
#             print "veo si cambio nombre editado:", ind.indicacion.nombre
#             dosisA = DosisAsignar.objects.get(asignacion = ind)
#             print "veo objetos dosisAsignar:",dosisA
#             print "veo input de dosis desde el POST:", request.POST[str(ind.id)+"dosis"]
#             dosisA.dosis=request.POST[str(ind.id)+"dosis"]
#             dosisA.save()
#             print "Veo si cambio el objeto elegido DOSISA:",dosisA
#             ind.save()
#             print "Veo si cambio el objeto elegido IND:",ind
#         indicaciones = Asignar.objects.filter(emergencia = id_emergencia,indicacion__tipo=tipo_ind)
#         print "Pastillas asignadas",indicaciones
#         mensaje = " Modificado Exitosamente"
#         info = {'mensaje':mensaje, 'emergencia':emer,'triage':triage,'indicaciones':indicaciones, 'tipo_ind':tipo_ind}
#         return render_to_response('atencion_ind_medica.html',info,context_instance=RequestContext(request))

#----------------------------------Gestion de Diagnostico Definitivo
@login_required(login_url='/')
def emergencia_diagnostico(request,id_emergencia):
    emer = get_object_or_404(Emergencia,id=id_emergencia)
    paci = Paciente.objects.filter(emergencia__id=id_emergencia)
    paci = paci[0]
    triage = Triage.objects.filter(emergencia=id_emergencia).order_by("-fechaReal")
    triage = triage[0]
    tipo_ind = 'diagnostico'
    at = Atencion.objects.filter(emergencia=id_emergencia)
    diags = EstablecerDiag.objects.filter(atencion=at[0])
    mensaje = ""
    info = {'mensaje':mensaje, 'emergencia':emer,'triage':triage,'diags':diags,'tipo_ind':tipo_ind}
    return render_to_response('atencion_diag.html',info,context_instance=RequestContext(request))
