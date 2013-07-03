from django.conf.urls import patterns, url, include

from app_emergencia import views

urlpatterns = patterns('app_emergencia.views',

    # Funciones de acceso a subfases de atencion

    url('^emergencia/atencion/indicacion/(?P<id_emergencia>.*)$','emergencia_indi'),
    
    # Acceso por default a antecedentes:
    url('^emergencia/atencion/(?P<id_emergencia>.*)$','emergencia_atencion'),

    #url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)$','emergencia_antecedentes_medico'),
    #url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/(?P<opcion>.*)$','emergencia_antecedentes_medico'),
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/agregar$','emergencia_antecedentes_agregar'),
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/modificar$','emergencia_antecedentes_modificar'),
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/eliminar$','emergencia_antecedentes_eliminar'),
 
      # Ingreso a antecedentes
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)$','emergencia_antecedentes_tipo'),
    url('^emergencia/antecedente/(?P<id_emergencia>.*)$','emergencia_antecedentes'),    

    # Ingreso a Examen fisico
    url('^emergencia/enviarcuerpo/(?P<id_emergencia>.*)/(?P<zona_cuerpo>.*)$','emergencia_enfermedad_enviarcuerpo'),
    url('^emergencia/cuerpo/(?P<id_emergencia>.*)/(?P<zona_cuerpo>.*)$','emergencia_enfermedad_zonacuerpo'),
    url('^emergencia/enfermedad/(?P<id_emergencia>.*)$','emergencia_enfermedad'),
    
    # Ingreso a Indicaciones Terapeuticas
    url('^emergencia/indicacionesT/(?P<id_emergencia>.*)$','emergencia_indicacionesT'),

    # Ingreso a Indicaciones Diagnosticas
    url('^emergencia/indicacionesD/(?P<id_emergencia>.*)$','emergencia_indicacionesD'),

    # Ingreso a Diagnostico Definitivo
    url('^emergencia/diagnostico/(?P<id_emergencia>.*)$','emergencia_diagnostico'),

    url('^emergencia/egreso/(?P<id_emergencia>.*)$','emergencia_egreso'),

    # Botones genericos de atencion:
    # Descargar historia medica 
    url('^emergencia/descarga/(?P<id_emergencia>.*)$','emergencia_descarga'),
)
