import logging

import os
from time import ctime
from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, current_app, flash, send_file, request #, make_response, abort
from flask_login import login_required, current_user


# from app.auth.decorators import admin_required
from app.auth.models import Users
# from app.models import Productos, CabecerasPresupuestos, Presupuestos, Parametros #, Proveedores
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
    return render_template("gestiones/alta_datos_cliente.html", form = form)
