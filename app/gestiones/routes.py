import logging

import os
from time import ctime
from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, current_app, flash, send_file, request #, make_response, abort
from flask_login import login_required, current_user


# from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Productos, CabecerasPresupuestos, Presupuestos, Parametros #, Proveedores
from . import gestiones_bp 
from .forms import CabeceraPresupuestoForm, ProductosPresupuestoForm #, BusquedaForm 

logger = logging.getLogger(__name__)

def control_vencimiento (fecha):
    if fecha < datetime.now():
        return "VENCIDO"

@gestiones_bp.route("/gestiones/altapresupuesto/", methods = ['GET', 'POST'])
@login_required
def alta_presupuesto():
    form = CabeceraPresupuestoForm()
    dias_a_vancer = timedelta(days = int(Parametros.get_by_tabla("dias_vencimiento").tipo_parametro))
    vencimiento_estimado = datetime.now() + dias_a_vancer

    if form.validate_on_submit():
        fecha_vencimiento = form.fecha_vencimiento.data
        nombre_cliente = form.nombre_cliente.data
        correo_electronico = form.correo_electronico.data
        
        cabecera = CabecerasPresupuestos(fecha_vencimiento = fecha_vencimiento,
                                            nombre_cliente = nombre_cliente,
                                            correo_electronico = correo_electronico,
                                            estado = 4,
                                            importe_total = 0.00,
                                            usuario_alta = current_user.email,
                                            usuario_modificacion = current_user.email
                                            )           
        cabecera.save()
        return redirect(url_for('gestiones.modificacion_productos_presupuesto', id_presupuesto = cabecera.id))
    
    return render_template("gestiones/alta_datos_cliente.html", form = form, vencimiento_estimado = vencimiento_estimado)
