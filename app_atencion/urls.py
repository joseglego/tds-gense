from django.conf.urls.defaults import patterns, include, url
from AM import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('app_atencion.views',

    url(r'^emergencia/atencion/(?P<id_emergencia>.*)$','atencion_atencion'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^emergencia/atencion/(?P<id_emergencia>.*)/cuerpo/(?P<perfil>\d+)$','atencion_enfermedad'),
	url(r'^emergencia/atencion/(?P<id_emergencia>.*)/indicaciones/(?P<perfil>\d+)$','atencion_indicaciones'),
	url(r'^emergencia/atencion/(?P<id_emergencia>.*)/diagnostico/(?P<perfil>\d+)$','atencion_diagnostico'),
					    
)
