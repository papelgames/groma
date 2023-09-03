import logging
import os

from flask import render_template, redirect, url_for, request, current_app, abort
from flask.helpers import flash
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

#from app.auth.decorators import admin_required
from app.auth.models import Users
from app.models import Personas
from . import abms_bp
from .forms import AltaPersonasForm

#from app.common.mail import send_email
from time import strftime, gmtime


logger = logging.getLogger(__name__)


@abms_bp.route("/abms/altapersonas/", methods = ['GET', 'POST'])
@login_required
def alta_persona():
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
    return render_template("abms/alta_datos_persona.html", form = form)


@abms_bp.route("/abms/actualizacionpersona/<int:id_persona>", methods = ['GET', 'POST'])
@login_required
def actualizacion_persona(id_persona):
    form=AltaPersonasForm()
    persona = Personas.get_by_id(id_persona)
    if form.validate_on_submit():
        persona.descripcion_nombre = form.descripcion_nombre.data
        persona.correo_electronico = form.correo_electronico.data
        persona.telefono = form.telefono.data
        persona.cuit = form.cuit.data
        persona.tipo_persona = form.tipo_persona.data 
        persona.nota = form.nota.data
        
        persona.save()
        flash("Se ha actualizado la persona correctamente.", "alert-success")
        return redirect(url_for('consultas.consulta_personas'))
       
    return render_template("abms/modificacion_datos_persona.html", form=form, persona = persona)
