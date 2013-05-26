# Manejo de Sesion
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Formularios
from django.core.context_processors import csrf
from django.template import RequestContext

# General HTML
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse, HttpResponseRedirect

# Manejo de Informacion de esta aplicacion
from forms import *
from models import *
	
# Create your views here.
def sesion_iniciar(request):
    if request.user.is_authenticated():
        usuario = request.user
        info = {'usuario':usuario}
        return render_to_response('loged.html',info)
    if request.method == 'POST':
        unombre = request.POST['unombre']
        uclave  = request.POST['uclave']
        user = authenticate(username=unombre,password=uclave)
        if user is not None:
            if user.is_active:
                login(request,user)
                info = {'usuario':user}
                siguiente = request.POST['next']
                if siguiente:
                    return redirect(siguiente)
                return render_to_response('loged.html',info)
        mensaje = 'Error: Usuario o Claves incorrectos'
        form = IniciarSesionForm()
        info = {'mensaje':mensaje,'form':form}
        return render_to_response('index.html',info,context_instance=RequestContext(request))
    form = IniciarSesionForm()
    info = {'form':form}
    return render_to_response('index.html',info,context_instance=RequestContext(request))

def sesion_cerrar(request):
    logout(request)
    return redirect('/')

def usuario_solicitar(request):
    mensaje = ""
    if request.method == 'POST':
        form = SolicitarCuenta(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            u_cedula           = pcd['cedula']
            u_nombres          = pcd['nombres']
            u_apellidos        = pcd['apellidos']
            u_tipo		         = pcd['tipo']
            u_sexo             = pcd['sexo']
            u_cel              = pcd['cod_cel'] + pcd['num_cel']
            u_direccion        = pcd['direccion']
            u_tlf_casa         = pcd['cod_casa'] + pcd['num_casa']
            u_email            = pcd['email']
            u_clave            = pcd['clave']
            u_clave0           = pcd['clave0']
            u_username         = pcd['nombres'] + '.' +pcd['apellidos']
            u_activo           = 'False'
            prueba = Usuario.objects.filter(cedula=u_cedula)
            prueba2 = (u_clave==u_clave0)
            if not prueba and prueba2:
                u = Usuario(username=u_username,cedula=u_cedula,first_name=u_nombres,habilitado=u_activo,last_name=u_apellidos,tipo=u_tipo,sexo=u_sexo,tlf_cel=u_cel,direccion=u_direccion,tlf_casa=u_tlf_casa,email=u_email,password=u_clave)
                active = False
                u.save() 	
                u.set_password = u_clave
                return redirect('/')
            else:
                mensaje = "Ya hay un usuario registrado con esa cedula o no hubo coincidencias en las contrasenas ingresadas"     
        info = {'form':form,'mensaje':mensaje}
        return render_to_response('solicitar.html',info,context_instance=RequestContext(request))
    form = SolicitarCuenta()
    info = {'form':form}
    return render_to_response('solicitar.html',info,context_instance=RequestContext(request))

@login_required(login_url='/')
def usario_listarPendientes(request):    
    listaP = Usuario.objects.filter(habilitado='False')
    info = {'listaP':listaP}
    return render_to_response('usuariosPendientes.html',info)

@login_required(login_url='/')
def usario_listar(request):    
    listaU = Usuario.objects.filter(habilitado='True')
    info = {'listaU':listaU}
    return render_to_response('listaUsuarios.html',info)

@login_required(login_url='/')
def usuario_rechazar(request,cedulaU):
    usuario = get_object_or_404(Usuario,cedula=cedulaU)
    usuario.delete()
    return redirect("/usuario/pendientes")

@login_required(login_url='/')
def usuario_aprobar(request,cedulaU):
    usuario = get_object_or_404(Usuario,cedula=cedulaU)
    return redirect("/usuario/pendientes")

@login_required(login_url='/')
def usuario_examinar(request,cedulaU):
    usuario = get_object_or_404(Usuario,cedula=cedulaU)
    info = {'usuario':usuario}
    return render_to_response('usuarioExaminar.html',info)



