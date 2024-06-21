from app.models import Gestiones, Estados

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
    gestion.id_estado = estado.id
    gestion.save()