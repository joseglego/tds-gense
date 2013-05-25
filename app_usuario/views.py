# Manejo de Sesion
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Formularios
from django.core.context_processors import csrf
from django.template import RequestContext

# General HTML
from django.shortcuts import render_to_response,redirect
from django.http import HttpResponse, HttpResponseRedirect

# Manejo de Informacion de esta aplicacion
from forms import *
from models import *

# Envio de Correos
from django.core.mail import EmailMessage

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
            u_tlf_casa         = pcd['cod_tlf_casa'] + pcd['num_tlf_casa']
            u_email            = pcd['email']
            u_clave            = pcd['clave']
            u_clave0           = pcd['clave0']
            prueba = Usuario.objects.filter(cedula=u_cedula)
            if not prueba:
                u = Usuario(cedula=u_cedula,nombres=u_nombres,apellidos=u_apellidos,tipo=u_tipo,sexo=u_sexo,tlf_cel=u_cel,direccion=u_direccion,tlf_casa=u_tlf_casa,email=u_email,clave=u_clave,clave0=u_clave0)
                u.save()
                return redirect('/')
            else:
                mensaje = "Ya hay un usuario registrado con esa cedula"                
        info = {'form':form,'mensaje':mensaje}
        return render_to_response('solicitar.html',info,context_instance=RequestContext(request))
    form = SolicitarCuenta()
    info = {'form':form}
    return render_to_response('solicitar.html',info,context_instance=RequestContext(request))

@login_required(login_url='/')
def clave_cambiar(request):
    mensaje = ""
    if request.method == 'POST':
        form = cambioClave(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            f_claveV          = pcd['claveV']
            f_clave           = pcd['clave']
            f_claveO          = pcd['claveO']
            usuario           = Usuario.objects.get(username=request.user)
            if usuario.check_password(f_claveV):
                if (f_clave == f_claveO):
                    usuario.set_password(f_clave)
                    usuario.save()
                    mensaje = "Clave cambiada"
                    form = cambioClave()
                    info = {'form':form,'mensaje':mensaje}
                    return render_to_response('cambiarClave.html',info,context_instance=RequestContext(request))                    
                else:
                    mensaje = "Las dos claves son distintas"
            else:
                mensaje = "La clave vieja no es correcta"
        else:
            mensaje = "Error con el formulario"
        info = {'form':form,'mensaje':mensaje}
        return render_to_response('cambiarClave.html',info,context_instance=RequestContext(request))
    form = cambioClave()
    info = {'form':form,'mensaje':mensaje}
    return render_to_response('cambiarClave.html',info,context_instance=RequestContext(request))

def clave_restablecer(request):
    mensaje = ""
    if request.method == 'POST':
        form = restablecerClave(request.POST)
        if form.is_valid():
            pcd = form.cleaned_data
            f_correo = pcd['correo']
            usuario = Usuario.objects.filter(email=f_correo)
            if len(usuario) == 0 :
                mensaje = "Correo Invalido"
            else:
                usuario = usuario[0]
                clave = User.objects.make_random_password()
                email = EmailMessage('[GenSE] Admin - Cambio de Clave','Estimado '+usuario.first_name+' '+usuario.last_name+'\n\nSe recibio una solicitud de cambiar su clave, la nueva clave es: '+clave+'\n\nSaludos\nAdministrador del Sistema', to=[f_correo]) 
                email.send()
                usuario.set_password(clave)
                usuario.save()
                mensaje = "Su nueva clave fue enviada al correo suministrado"
                form = restablecerClave()
                info = {'form':form,'mensaje':mensaje}
                return render_to_response('restablecerClave.html',info,context_instance=RequestContext(request))
        else:
            mensaje = "Error con el formulario"
    form = restablecerClave()
    info = {'form':form,'mensaje':mensaje}
    return render_to_response('restablecerClave.html',info,context_instance=RequestContext(request))
