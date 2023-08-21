import logging
import os

from flask import render_template, redirect, url_for, request, current_app, abort
from flask.helpers import flash
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename

#from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Productos, Proveedores
from . import abms_bp
from .forms import BusquedaForm, ProductosForm, ProveedoresForm, ProductosMasivosForm #, ProveedoresConsultaForm

#from app.common.mail import send_email
from time import strftime, gmtime


logger = logging.getLogger(__name__)



@abms_bp.route("/abms/altaindividual", methods = ['GET', 'POST'])
@login_required
def alta_individual():
    form=ProductosForm()
  
    return render_template("abms/alta_individual.html", form=form)
