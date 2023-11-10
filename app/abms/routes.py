import logging
import os

from flask import render_template, redirect, url_for, request, current_app, abort
from flask.helpers import flash
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required, not_initial_status
from app.auth.models import Users
from app.models import Personas, TiposGestiones, TiposBienes, Permisos, Roles
from . import abms_bp
from .forms import AltaPersonasForm, TiposForm, PermisosForm, RolesForm

#from app.common.mail import send_email
from time import strftime, gmtime


logger = logging.getLogger(__name__)

#creo una tupla para usar en el campo select del form que quiera que necesite los tipo de gestiones
def permisos_select():
    permisos = Permisos.get_all()
    select_permisos =[( '','Seleccionar permiso')]
    for rs in permisos:
        sub_select_permisos = (str(rs.id), rs.descripcion)
        select_permisos.append(sub_select_permisos)
    return select_permisos


@abms_bp.route("/abms/altapersonas/", methods = ['GET', 'POST'])
@login_required
@not_initial_status
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
                           nota = nota,
                           usuario_alta = current_user.username)
        persona.save()
        flash("Se ha creado la persona correctamente.", "alert-success")
        return redirect(url_for('gestiones.gestiones'))
    return render_template("abms/alta_datos_persona.html", form = form)


@abms_bp.route("/abms/actualizacionpersona/<int:id_persona>", methods = ['GET', 'POST'])
@login_required
@not_initial_status
def actualizacion_persona(id_persona):
    form=AltaPersonasForm()
    persona = Personas.get_by_id(id_persona)
    if form.validate_on_submit():
        form.populate_obj(persona)
        persona.usuario_modificacion = current_user.username
        
        persona.save()
        flash("Se ha actualizado la persona correctamente.", "alert-success")
        return redirect(url_for('consultas.consulta_personas'))
    
    for campo in list(request.form.items())[1:]:
        data_campo = getattr(form,campo[0]).data
        setattr(persona,campo[0], data_campo)

    return render_template("abms/modificacion_datos_persona.html", form=form, persona = persona)

@abms_bp.route("/abms/altatipogestiones/", methods = ['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def alta_tipo_gestion():
    form = TiposForm()
    tipos = TiposGestiones.get_all()
    if form.validate_on_submit():
        descripcion = form.tipo.data

        tipo_gestion = TiposGestiones(descripcion=descripcion)

        tipo_gestion.save()
        flash("Nuevo tipo de gestión creada", "alert-success")
        return redirect(url_for('abms.alta_tipo_gestion'))

    return render_template("abms/alta_tipo_gestion.html", form=form, tipos=tipos)

@abms_bp.route("/abms/altatipobienes/", methods = ['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def alta_tipo_bien():
    form = TiposForm()
    tipos = TiposBienes.get_all()
    if form.validate_on_submit():
        descripcion = form.tipo.data

        tipo_bien = TiposBienes(descripcion=descripcion)

        tipo_bien.save()
        flash("Nuevo tipo de bien creado", "alert-success")
        return redirect(url_for('abms.alta_tipo_bien'))

    return render_template("abms/alta_tipo_bien.html", form=form, tipos=tipos)

@abms_bp.route("/abms/altapermisos/", methods = ['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def alta_permiso():
    form = PermisosForm()
    permisos = Permisos.get_all()
    if form.validate_on_submit():
        descripcion = form.permiso.data

        permiso = Permisos(descripcion=descripcion)

        permiso.save()
        flash("Nuevo permiso creado", "alert-success")
        return redirect(url_for('abms.alta_permiso'))

    return render_template("abms/alta_permisos.html", form=form, permisos=permisos)

@abms_bp.route("/admin/crearroles/", methods=['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def crear_roles():
    descripcion_rol = request.args.get('rol','')
    permisos_en_rol = Roles.get_all_by_descripcion(descripcion_rol)
    
    form = RolesForm()
    form.id_permiso.choices= permisos_select()

    if form.validate_on_submit():
        id_permiso = form.id_permiso.data
        descripcion = form.descripcion.data
        
        permiso=Permisos.get_by_id(id_permiso)
        
        rol = Roles(descripcion=descripcion)

        permiso.roles.append(rol)

        permiso.save()
        
        flash ('Permiso en rol correctamente', 'alert-success')
        return redirect(url_for('abms.crear_roles', rol = descripcion))
    return render_template("abms/roles.html", form=form, permisos_en_rol=permisos_en_rol)

