from app.models import Gestiones, Estados, GestionesDeTareas
from flask_login import current_user

def calcular_estado_gestion(id_gestion):
    gestion = Gestiones.get_by_id(id_gestion)
    '''
    Estados:
    1=Gestion iniciada
    2=Sin tareas asignadas
    3=Tiene tareas pendientes
    4=Finalizado 
    '''
    if id_gestion == None:
        estado = Estados.get_first_by_clave_tabla(1,'gestiones')
        return estado.id
    estado = Estados.get_first_by_clave_tabla(4,'gestiones')
    if not gestion.gestiones_de_tareas:
        estado = Estados.get_first_by_clave_tabla(2,'gestiones')
        gestion.id_estado = estado.id
        gestion.save()
    for tarea in gestion.gestiones_de_tareas:
        if tarea.fecha_fin == None:
            estado = Estados.get_first_by_clave_tabla(3,'gestiones')
            gestion.id_estado = estado.id
            gestion.save()
            break
    gestion.id_estado = estado.id
    gestion.save()

def calcular_estado_gestion_tarea(id_gestion_tarea):
    '''
    Estados:
    1=Pendiente
    2=Sin iniciar
    3=Finalizado 
    '''
    tarea_pendiente = GestionesDeTareas.get_all_by_id_gestion_de_tarea(id_gestion_tarea)

    if not tarea_pendiente.fecha_inicio:
        estado = Estados.get_first_by_clave_tabla(2,'gestionesdetareas')
        tarea_pendiente.id_estado = estado.id
        tarea_pendiente.save()
    elif not tarea_pendiente.fecha_fin:
        estado = Estados.get_first_by_clave_tabla(1,'gestionesdetareas')
        tarea_pendiente.id_estado = estado.id
        tarea_pendiente.save()
    else:
        estado = Estados.get_first_by_clave_tabla(3,'gestionesdetareas')
        tarea_pendiente.id_estado = estado.id
        tarea_pendiente.save()

def listar_endpoints(app):
    """
    Lista todos los endpoints registrados en la aplicación Flask.
    """
    endpoints = []

    for rule in app.url_map.iter_rules():
        endpoints.append({'descripcion' :rule.endpoint, 
                            'usuario_alta':current_user.username})
    return endpoints
