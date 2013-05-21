# Manejo de Sesion
2from django.contrib.auth import authenticate, login, logout

# Formularios
from django.core.context_processors import csrf
from django.template import RequestContext

# General HTML
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
