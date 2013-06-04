from django.conf.urls import patterns, url, include

from app_emergencia import views

urlpatterns = patterns('app_emergencia.views',

    # Funciones de acceso a subfases de atencion
    
    # Acceso por default a antecedentes:
    url('^emergencia/atencion/(?P<id_emergencia>.*)$','emergencia_atencion'), 
    
    # Ingreso a antecedentes
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)$','emergencia_antecedentes'),
    
    # Ingreso a Examen fisico
    url('^emergencia/enfermedad/(?P<id_emergencia>.*)$','emergencia_enfermedad'),
    
    # Ingreso a Indicaciones Terapeuticas
    url('^emergencia/indicacionesT/(?P<id_emergencia>.*)$','emergencia_indicacionesT'),

    # Ingreso a Indicaciones Diagnosticas
    url('^emergencia/indicacionesD/(?P<id_emergencia>.*)$','emergencia_indicacionesD'),

    # Ingreso a Diagnostico Definitivo
    url('^emergencia/diagnostico/(?P<id_emergencia>.*)$','emergencia_diagnostico'),


    # Botones genericos de atencion:
    # Descargar historia medica 
    url('^emergencia/descarga/(?P<id_emergencia>.*)$','emergencia_descarga'),
)
