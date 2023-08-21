import logging

from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, abort, current_app, flash, request
from flask_login import login_required, current_user

#from app.auth.decorators import admin_required
from app.auth.models import Users
from app.models import Gestiones, Cobros, ImportesCobros, Estados, TiposGestiones, Observaciones, Personas

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

    return render_template("consultas/consulta_productos.html", form = form, criterio = criterio )

