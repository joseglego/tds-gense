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
	url(r'^',include('app_atencion.urls')),

    # Emergencias
    url('^emergencia/agregar$','app_emergencia.views.emergencia_agregar'),
    url('^emergencia/listar$','app_emergencia.views.emergencia_listar'),
    url('^emergencia/(?P<idE>\d+)/t(?P<vTriage>\d+)$','app_emergencia.views.emergencia_aplicarTriage'),
#    url('^emergencia/(?P<idE>\d+)/triage/calcular$','app_emergencia.views.emergencia_calcularTriage'),   

		# Paciente
		url('^paciente/listarPacientes$','app_paciente.views.paciente_listarPacientes'),    
                       
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
