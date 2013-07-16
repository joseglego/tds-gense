from django.conf.urls import patterns, url, include

from app_emergencia import views

urlpatterns = patterns('app_emergencia.views',

    # Funciones de acceso a subfases de atencion

    # Acceso a Enfermedad Actual
    url('^emergencia/enf_actual/(?P<id_emergencia>.*)$','emergencia_enfermedad_actual'),
    
    # Acceso a Atencion
    url('^emergencia/atencion/(?P<id_emergencia>.*)$','emergencia_atencion'),
    
    # Acciones Antecedentes
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/agregar$','emergencia_antecedentes_agregar'),
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/modificar$','emergencia_antecedentes_modificar'),
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)/eliminar$','emergencia_antecedentes_eliminar'),
 
      # Ingreso a antecedentes
    url('^emergencia/antecedentes/(?P<id_emergencia>.*)/(?P<tipo_ant>.*)$','emergencia_antecedentes_tipo'),
    url('^emergencia/antecedente/(?P<id_emergencia>.*)$','emergencia_antecedentes'),

    # Ingreso a Examen fisico
    url('^emergencia/enviarcuerpo/(?P<id_emergencia>.*)/(?P<parte_cuerpo>.*)$','emergencia_enfermedad_enviarcuerpo'),
    url('^emergencia/partecuerpo/(?P<id_emergencia>.*)/(?P<parte_cuerpo>.*)$','emergencia_enfermedad_partecuerpo'),
    url('^emergencia/cuerpo/(?P<id_emergencia>.*)/(?P<zona_cuerpo>.*)$','emergencia_enfermedad_zonacuerpo'),
    url('^emergencia/enfermedad/(?P<id_emergencia>.*)$','emergencia_enfermedad'),

    # Ingreso a Indicaciones-----------------------------------------------------------------------------
    # Acciones:
    # Listar detalles indicacion:
    url('^emergencia/infoInd/(?P<id_asignacion>.*)/(?P<tipo_ind>.*)$','emergencia_indicacion_info'),
    # Agregar 
    url('^emergencia/indicaciones/(?P<id_emergencia>.*)/(?P<tipo_ind>.*)/agregar$','emergencia_indicaciones_agregar'),
    # Eliminar
    url('^emergencia/indicaciones/(?P<id_emergencia>.*)/(?P<tipo_ind>.*)/eliminar$','emergencia_indicaciones_eliminar'),
    # Modificar Medicamento
    # url('^emergencia/indicaciones/(?P<id_emergencia>.*)/(?P<tipo_ind>.*)/modificar$','emergencia_indicaciones_modificar'),

    # Ingreso a Indicaciones Especializadas
    url('^emergencia/indicaciones/(?P<id_emergencia>.*)/(?P<tipo_ind>.*)$','emergencia_indicaciones'),

    # Ingreso a Indicaciones general
    url('^emergencia/indi/(?P<id_emergencia>.*)$','emergencia_indicaciones_ini'),

    #-----------------------------------------------------------------------fIND

    # Ingreso a Diagnostico Definitivo
    url('^emergencia/diagnostico/(?P<id_emergencia>.*)$','emergencia_diagnostico'),

    # Botones genericos de atencion:
    # Descargar historia medica 
    url('^emergencia/descarga/(?P<id_emergencia>.*)$','emergencia_descarga'),
)
