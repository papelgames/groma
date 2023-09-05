import logging

import os
from time import ctime
from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, current_app, flash, send_file, request #, make_response, abort
from flask_login import login_required, current_user

from app.auth.decorators import admin_required
from app.auth.models import Users
from app.models import Personas, TiposGestiones, TiposBienes, Gestiones, Observaciones, Cobros
from . import gestiones_bp 
from .forms import AltaGestionesForm, BusquedaForm, CobrosForm

logger = logging.getLogger(__name__)

def control_vencimiento (fecha):
    if fecha < datetime.now():
        return "VENCIDO"

#creo una tupla para usar en el campo select del form que quiera que necesite los tipo de gestiones
def tipo_gestion_select():
    tipos_gestiones = TiposGestiones.get_all()
    select_tipo_gestion =[( '','Seleccionar tipo de gestión')]
    for rs in tipos_gestiones:
        sub_select_tipo_gestion = (str(rs.id), rs.descripcion)
        select_tipo_gestion.append(sub_select_tipo_gestion)
    return select_tipo_gestion

#creo una tupla para usar en el campo select del form que quiera que necesite los tipo de bienes
def tipo_bien_select():
    tipos_bienes = TiposBienes.get_all()
    select_tipo_bien =[( '','Seleccionar tipo de bien')]
    for rs in tipos_bienes:
        sub_select_tipo_bien = (str(rs.id), rs.descripcion)
        select_tipo_bien.append(sub_select_tipo_bien)
    return select_tipo_bien


@gestiones_bp.route("/gestiones/altagestiones/<int:id_cliente>", methods = ['GET', 'POST'])
@login_required
def alta_gestiones(id_cliente):
    if not id_cliente:
        return redirect(url_for('gestiones.gestiones'))
    form = AltaGestionesForm()                                                                                                                   
    clientes = Personas.get_all()
    form.id_tipo_gestion.choices = tipo_gestion_select()
    form.id_tipo_bienes.choices = tipo_bien_select()
    
    if form.validate_on_submit():
        id_titular = form.id_titular.data.split('|',)[0]
        ubicacion_gestion = form.ubicacion_gestion.data 
        id_tipo_bienes = form.id_tipo_bienes.data
        fecha_inicio_gestion = form.fecha_inicio_gestion.data
        fecha_probable_medicion = form.fecha_probable_medicion.data
        id_tipo_gestion = form.id_tipo_gestion.data
        id_dibujante = form.id_dibujante.data.split('|',)[0]
        estado_parcelario = form.estado_parcelario.data
        numero_partida = form.numero_partida.data
        observacion = form.observacion.data
        
        descripcion_nombre = form.descripcion_nombre.data
        cuit = form.cuit.data
        
        if (descripcion_nombre and cuit) and not id_titular:
            nuevo_titular = Personas(descripcion_nombre = descripcion_nombre,
                                     cuit = cuit) 
            nuevo_titular.save()
            id_titular = nuevo_titular.id
           
        nueva_gestion = Gestiones(id_cliente = id_cliente,
                                id_titular = id_titular,
                                ubicacion_gestion = ubicacion_gestion, 
                                id_tipo_bienes = id_tipo_bienes,
                                fecha_inicio_gestion = fecha_inicio_gestion,
                                fecha_probable_medicion = fecha_probable_medicion,
                                id_tipo_gestion = id_tipo_gestion,
                                id_dibujante = id_dibujante,
                                estado_parcelario = estado_parcelario,
                                numero_partida = numero_partida
                                )
        observacion_gestion = Observaciones(
            observacion = observacion
        )

        if observacion:
            nueva_gestion.observaciones = observacion_gestion
        nueva_gestion.save()

        flash("Se ha creado la gestion correctamente.", "alert-success")
        return redirect(url_for('public.index'))
    return render_template("gestiones/alta_gestiones.html", form = form, clientes = clientes)

@gestiones_bp.route("/gestiones/gestiones/<criterio>", methods = ['GET', 'POST'])
@gestiones_bp.route("/gestiones/gestiones/", methods = ['GET', 'POST'])
@login_required
def gestiones(criterio = ""):
    form = BusquedaForm()
    lista_de_personas = []
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    if form.validate_on_submit():
        buscar = form.buscar.data
        return redirect(url_for("gestiones.gestiones", criterio = buscar))
    if criterio.isdigit() == True:
        lista_de_personas = Personas.get_by_cuit(criterio)
    elif criterio == "":
        pass
    else:
        lista_de_personas = Personas.get_like_descripcion_all_paginated(criterio, page, per_page)
        if len(lista_de_personas.items) == 0:
            lista_de_personas =[]

    return render_template("gestiones/gestiones.html", form = form, criterio = criterio, lista_de_personas= lista_de_personas )

@gestiones_bp.route("/gestiones/altacobroscabecera/<int:id_gestion>", methods = ['GET', 'POST'])
@login_required
@admin_required
def alta_cobros_cavecera(id_gestion):
    if not id_gestion:
        return redirect(url_for('gestiones.gestiones'))
    form = CobrosForm()                                                                                                                   
    
    if form.validate_on_submit():
        fecha_probable_cobro = form.fecha_probable_cobro.data
        fecha_vencimiento = form.fecha_vencimiento.data
        importe_total = form.importe_total.data
        moneda = form.moneda.data        
        observacion = form.observacion.data
        
        nuevo_cobro = Cobros(fecha_probable_cobro = fecha_probable_cobro,
                             fecha_vencimiento = fecha_vencimiento,
                             importe_total = importe_total,
                             moneda = moneda)        
        observacion_gestion = Observaciones(
            id_gestion = id_gestion,
            observacion = observacion
        )

        if observacion:
            nuevo_cobro.observaciones = observacion_gestion
        nuevo_cobro.save()

        flash("El cobro se a cargado proyectado correctamente.", "alert-success")
        return redirect(url_for('public.index'))
    return render_template("gestiones/alta_cobros_cabecera.html", form = form)


@gestiones_bp.route('/gestiones/datosgestion')
@login_required
def datosgestion():
    descripcion = "Casa" 
    nuevotpgestion = TiposBienes(descripcion = descripcion)
    print(descripcion)
    nuevotpgestion.save()

    flash('Grabado','alert-success')
    return redirect(url_for('public.index'))