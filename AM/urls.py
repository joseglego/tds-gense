from django.conf.urls import patterns, include, url
from AM import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ## APLICACIONES PROPIAS
    # Usuario
    url('^$','app_usuario.views.sesion_iniciar'),
    url('^sesion/cerrar$','app_usuario.views.sesion_cerrar'),
    url('^usuario/solicitar$','app_usuario.views.usuario_solicitar'),
    url('^usuario/pendientes$','app_usuario.views.usario_listarPendientes'),
    url('^usuario/listar$','app_usuario.views.usario_listar'),
    url('^usuario/pendientes/(?P<cedulaU>\d+)/aprobar$','app_usuario.views.usuario_aprobar'),
    url('^usuario/pendientes/(?P<cedulaU>\d+)/rechazar$','app_usuario.views.usuario_rechazar'),
    url('^usuario/pendientes/(?P<cedulaU>\d+)/examinar$','app_usuario.views.usuario_examinar'),
    url('^usuario/clave$','app_usuario.views.clave_cambiar'),
    url('^usuario/restablecer$','app_usuario.views.clave_restablecer'),
    url(r'^',include('app_atencion.urls')),


    # Emergencias
    url('^emergencia/agregar$','app_emergencia.views.emergencia_agregar'),
    url('^emergencia/listar$','app_emergencia.views.emergencia_listar'),
    url('^emergencia/(?P<idE>\d+)/t(?P<vTriage>\d+)$','app_emergencia.views.emergencia_aplicarTriage'),
    url('^emergencia/(?P<idE>\d+)/triage/calcular$','app_emergencia.views.emergencia_calcularTriage'),   
    url('^emergencia/(?P<idE>\d+)/daralta$','app_emergencia.views.emergencia_darAlta'),   
    # Paciente
    url('^paciente/listarPacientes$','app_paciente.views.paciente_listarPacientes'),    
    url('^paciente/buscarjson/(?P<ced>\w+)$','app_paciente.views.buscarPacienteJson'),                           
    ## COSAS DJANGISTICAS
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # Media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # Static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),


    # Examples:
    # url(r'^$', 'AM.views.home', name='home'),
    # url(r'^AM/', include('AM.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
