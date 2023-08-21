import logging

from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, abort, current_app, flash, request
from flask_login import login_required, current_user

#from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Productos, CabecerasPresupuestos, Presupuestos, Parametros #, Proveedores

from . import consultas_bp 
from .forms import BusquedaForm


logger = logging.getLogger(__name__)

def control_vencimiento (fecha):
    if fecha < datetime.now():
        return "VENCIDO"

@consultas_bp.route("/consultas/consultaproducto/<criterio>", methods = ['GET', 'POST'])
@consultas_bp.route("/consultas/consultaproducto/", methods = ['GET', 'POST'])
@login_required
def consulta_productos(criterio = ""):
    form = BusquedaForm()
    lista_de_productos = []
    page = int(request.args.get('page', 1))
    per_page = current_app.config['ITEMS_PER_PAGE']
    if form.validate_on_submit():
        buscar = form.buscar.data
        return redirect(url_for("consultas.consulta_productos", criterio = buscar))
    
    if criterio.isdigit() == True:
        producto_caro = Productos.get_by_codigo_de_barras_caro(criterio)
        if producto_caro: 
            lista_de_productos = Productos.get_by_id_completo(producto_caro.id)
            # print(lista_de_productos)
    elif criterio == "":
        pass
    else:
        lista_de_productos = Productos.get_like_descripcion_all_paginated(criterio,page, per_page)
        if len(lista_de_productos.items) == 0:
            lista_de_productos =[]
          
    cantidad_dias_actualizacion = timedelta(days = int(Parametros.get_by_tabla("dias_actualizacion").tipo_parametro)) 
    fecha_tope = datetime.now() - cantidad_dias_actualizacion
    
    return render_template("consultas/consulta_productos.html", form = form, lista_de_productos=lista_de_productos, criterio = criterio, fecha_tope = fecha_tope )

