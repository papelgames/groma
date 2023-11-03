import logging
import os

from flask import render_template, redirect, url_for, abort, current_app, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required, not_initial_status
from app.auth.models import Users
from app.models import PermisosPorUsuarios
from . import admin_bp
from .forms import UserAdminForm, PermisosUserForm

logger = logging.getLogger(__name__)


@admin_bp.route("/admin/")
@login_required
@admin_required
@not_initial_status
def index():
    return render_template("admin/index.html")

@admin_bp.route("/admin/users/")
@login_required
@admin_required
@not_initial_status
def list_users():
    users = Users.get_all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/admin/user/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def update_user_form(user_id):
    # Aquí entra para actualizar un usuario existente
    user = Users.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    # Crea un formulario inicializando los campos con
    # los valores del usuario.
    form = UserAdminForm(obj=user)
    if form.validate_on_submit():
        # Actualiza los campos del usuario existente
        # user.is_admin = form.is_admin.data
        # user.es_dibujante = form.es_dibujante.data
        form.populate_obj(user)
        user.save()
        logger.info(f'Guardando el usuario {user_id}')
        return redirect(url_for('admin.list_users'))
    return render_template("admin/user_form.html", form=form, user=user)


@admin_bp.route("/admin/user/delete/<int:user_id>/", methods=['POST', ])
@login_required
@admin_required
@not_initial_status
def delete_user(user_id):
    logger.info(f'Se va a eliminar al usuario {user_id}')
    user = Users.get_by_id(user_id)
    if user is None:
        logger.info(f'El usuario {user_id} no existe')
        abort(404)
    user.delete()
    logger.info(f'El usuario {user_id} ha sido eliminado')
    return redirect(url_for('admin.list_users'))

@admin_bp.route("/admin/asignacionpermisos/<int:user_id>/", methods=['GET', 'POST'])
@login_required
@admin_required
@not_initial_status
def asignacion_permisos(user_id):
    # Aquí entra para actualizar un usuario existente
    user = Users.get_by_id(user_id)
    permisos_en_usuario = PermisosPorUsuarios.get_all_by_id_user(user_id)
    form = PermisosUserForm()
    if form.validate_on_submit():
        descripcion = form.descripcion.data

        permisos_usuarios = PermisosPorUsuarios(descripcion=descripcion)

        user.permisos_usuario.append(permisos_usuarios)

        user.save()
        flash ('Permiso asignado correctamente', 'alert-success')
        return redirect(url_for('admin.asignacion_permisos', user_id = user_id))
    return render_template("admin/permisos_usuarios.html", form=form, user=user, permisos_en_usuario=permisos_en_usuario)
