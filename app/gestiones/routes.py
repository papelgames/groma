import logging

import os
from time import ctime
from datetime import date, datetime, timedelta

from flask import render_template, redirect, url_for, current_app, flash, send_file, request #, make_response, abort
from flask_login import login_required, current_user


# from app.auth.decorators import admin_required
from app.auth.models import Users
from app.models import Personas #, Proveedores
from . import gestiones_bp 
from .forms import AltaPersonasForm 

logger = logging.getLogger(__name__)

def control_vencimiento (fecha):
    if fecha < datetime.now():
        return "VENCIDO"

@gestiones_bp.route("/gestiones/altapersonas/", methods = ['GET', 'POST'])
@login_required
def alta_personas():
    form = AltaPersonasForm()                                                                                                                   

    if form.validate_on_submit():
        descripcion_nombre = form.descripcion_nombre.data
        correo_electronico = form.correo_electronico.data
        telefono = form.telefono.data
        cuit = form.cuit.data
        tipo_persona = form.tipo_persona.data 
        nota = form.nota.data
        persona_por_cuit = Personas.get_by_cuit(cuit)
        if persona_por_cuit:
            flash ("Ya existe la persona","alert-warning")
            return redirect(url_for('public.index'))

        persona = Personas(descripcion_nombre= descripcion_nombre,
                           correo_electronico = correo_electronico,
                           telefono = telefono,
                           cuit = cuit,
                           tipo_persona = tipo_persona,
                           nota = nota)
        persona.save()
        flash("Se ha creado la persona correctamente.", "alert-success")
        return redirect(url_for('public.index'))
    return render_template("gestiones/alta_datos_cliente.html", form = form)
