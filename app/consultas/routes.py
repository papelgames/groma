import logging

from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, abort, current_app, flash, request
from flask_login import login_required, current_user

from app.auth.decorators import admin_required, not_initial_status, nocache
from app.auth.models import Users
from app.models import Gestiones, Cobros, ImportesCobros, Estados, TiposGestiones, Observaciones, Personas, GestionesDeTareas

from . import consultas_bp 
from .forms import BusquedaForm


logger = logging.getLogger(__name__)

def control_vencimiento (fecha):
    if fecha < datetime.now():
        return "VENCIDO"

@consultas_bp.route("/consultas/consultapersonas/<criterio>", methods = ['GET', 'POST'])
@consultas_bp.route("/consultas/consultapersonas/", methods = ['GET', 'POST'])
@login_required
@not_initial_status
@nocache
def consulta_personas(criterio = ""):
    form = BusquedaForm()
    lista_de_personas = []
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    if form.validate_on_submit():
        buscar = form.buscar.data
        return redirect(url_for("consultas.consulta_personas", criterio = buscar))
    if criterio.isdigit() == True:
        lista_de_personas = Personas.get_by_cuit(criterio)
    elif criterio == "":
        pass
    else:
        lista_de_personas = Personas.get_like_descripcion_all_paginated(criterio, page, per_page)
        if len(lista_de_personas.items) == 0:
            lista_de_personas =[]

    return render_template("consultas/consulta_personas.html", form = form, criterio = criterio, lista_de_personas= lista_de_personas )

@consultas_bp.route("/consultas/listagestiones/<criterio>", methods = ['GET', 'POST'])
@consultas_bp.route("/consultas/listagestiones/", methods = ['GET', 'POST'])
@login_required
@not_initial_status
@nocache
def lista_gestiones(criterio = ""):
    form = BusquedaForm()
    
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    gestiones = Gestiones.get_all_paginated(page, per_page)

    cuit_cliente = request.args.get('cuit','')
    
    if len(gestiones.items) == 0:
            gestiones =[]

    if form.validate_on_submit():
        buscar = form.buscar.data
        return redirect(url_for("consultas.lista_gestiones", criterio = buscar))
    
    if criterio.isdigit() == True:
        gestiones = Gestiones.get_by_id(criterio)
    elif cuit_cliente:
        id_cliente = Personas.get_by_cuit(cuit_cliente)
        gestiones = Gestiones.get_gestiones_by_id_cliente_all_paginated(id_cliente.id)
        if len(gestiones.items) == 0:
            gestiones =[]

    elif criterio == "":
        pass
    else:
        gestiones = Gestiones.get_like_descripcion_all_paginated(criterio, page, per_page)
        if len(gestiones.items) == 0:
            gestiones =[]
    
    return render_template("consultas/lista_gestiones.html", form = form, criterio = criterio, gestiones = gestiones )


@consultas_bp.route("/consultas/cobro/")
@login_required
@admin_required
@not_initial_status
def cobro():
    id_gestion = request.args.get('id_gestion','')
    cobro_individual = Gestiones.get_by_id(id_gestion)
    
    if cobro_individual:
        importe_cobrado = sum(importe_cobro.importe for importe_cobro in cobro_individual.cobro.importes_cobros)
        return render_template("consultas/cobro.html", cobro_individual = cobro_individual, importe_cobrado=importe_cobrado)
    flash("La gestión no tiene dado de alta un presupuesto","alert-warning")
    return redirect(url_for("consultas.lista_gestiones", criterio = id_gestion))

@consultas_bp.route("/consultas/vercobros/", methods = ['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def ver_cobros():
    id_gestion = request.args.get('id_gestion','')

    hoy = datetime.today()
    cobros = Gestiones.get_by_id(id_gestion)
    return render_template("consultas/ver_cobros.html", cobros=cobros, hoy=hoy)


@consultas_bp.route("/consultas/caratula/")
@login_required
@not_initial_status
def caratula():
    id_gestion = request.args.get('id_gestion','')
    gestion = Gestiones.get_by_id(id_gestion)
    return render_template("consultas/caratula.html", gestion = gestion)
    
@consultas_bp.route("/consultas/bitacora/")
@login_required
@not_initial_status
@nocache
def bitacora():
    id_gestion = request.args.get('id_gestion','')
    gestion = Gestiones.get_by_id(id_gestion)
    bitacora_completa = Observaciones.get_all_by_id_gestion(id_gestion)
    return render_template("consultas/bitacora.html", gestion = gestion, bitacora_completa=bitacora_completa)
    
@consultas_bp.route("/consultas/tareaspendientes/", methods = ['GET', 'POST'])
@login_required
@not_initial_status
@nocache
def tareas_pendientes():
    id_gestion = request.args.get('id_gestion','')
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    
    if id_gestion:
        tareas_pendientes_por_gestion = GestionesDeTareas.get_gestiones_tareas_pendientes__por_gestiones_all_paginated(id_gestion, page, per_page)
    else:
        tareas_pendientes_por_gestion = GestionesDeTareas.get_gestiones_tareas_pendientes_all_paginated(page, per_page)
    
    return render_template("consultas/tareas_pendientes.html", tareas_pendientes_por_gestion = tareas_pendientes_por_gestion )

@consultas_bp.route("/consultas/reportes/")
@login_required
@not_initial_status
@nocache
def reportes():
    #elijo un reporte a mostrar con un string
    reporte = request.args.get('reporte','')
    graficos = [[ 'tixm','Cantidad de tareas por mes'], 
                [ 'qtxe','Tareas por estados'], 
                [ 'qgxc','Gestiones por cliente'], 
                [ 'qgpxc','Gestiones pendientes por cliente']]
    
    #cantidad de tareas ingresadas por mes grafico de barras 
    if reporte == 'tixm':
        q_inicio_x_mes = GestionesDeTareas.get_q_iniciadas_x_mes()
        diccionario = {'label':[],'valor':[]}
        id_canvas = 'barChart'
        id_div_chartdata = 'chartDataBar'
        label_grafico = 'Tareas iniciadas'
        
        for datos in q_inicio_x_mes:
            if datos.year:
                diccionario['label'].append(f'{datos.month}-{datos.year}') 
                diccionario['valor'].append(datos.count)
        return render_template("/consultas/reportes.html", diccionario=diccionario, 
                               graficos = graficos, 
                               id_canvas = id_canvas,
                               id_div_chartdata = id_div_chartdata,
                               label_grafico = label_grafico )    
    #cantidad de tareas por estado, grafico de tortas
    elif reporte == 'qtxe':
        q_x_estados = GestionesDeTareas.get_q_x_estado()
        diccionario = {'label':[], 'valor':[]}
        id_canvas = 'pieChart'
        id_div_chartdata = 'chartDataPie'
        label_grafico = 'Tareas por estado'
        for datos in q_x_estados:
            diccionario['label'].append(datos.estado)
            diccionario['valor'].append(datos.count)
        return render_template("/consultas/reportes.html", diccionario=diccionario, 
                               graficos = graficos, 
                               id_canvas = id_canvas,
                               id_div_chartdata = id_div_chartdata,
                               label_grafico = label_grafico)
    #cantidad de gestiones por cliente
    elif reporte == 'qgxc':
        q_x_gestiones_x_clientes = Gestiones.get_q_x_clientes()
        diccionario = {'label':[], 'valor':[]}
        id_canvas = 'barChart'
        id_div_chartdata = 'chartDataBar'
        label_grafico = 'Gestiones por cliente'
        for datos in q_x_gestiones_x_clientes:
            diccionario['label'].append(datos.cliente)
            diccionario['valor'].append(datos.count)
        return render_template("/consultas/reportes.html", diccionario=diccionario, 
                               graficos = graficos, 
                               id_canvas = id_canvas,
                               id_div_chartdata = id_div_chartdata,
                               label_grafico = label_grafico)
    #cantidad de getiones pendientes por cliente
    elif reporte == 'qgpxc':
        q_x_gestiones_pendientes_x_clientes = Gestiones.get_q_x_clientes(4)
        diccionario = {'label':[], 'valor':[]}
        id_canvas = 'barChart'
        id_div_chartdata = 'chartDataBar'
        label_grafico = 'Gestiones pendientes por cliente'
        for datos in q_x_gestiones_pendientes_x_clientes:
            diccionario['label'].append(datos.cliente)
            diccionario['valor'].append(datos.count)
        return render_template("/consultas/reportes.html", diccionario=diccionario, 
                               graficos = graficos, 
                               id_canvas = id_canvas,
                               id_div_chartdata = id_div_chartdata,
                               label_grafico = label_grafico) 
    return render_template("/consultas/reportes.html", graficos= graficos)