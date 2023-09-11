from flask import (render_template, redirect, url_for,
                   request, current_app)
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import true
from werkzeug.urls import url_parse
from flask.helpers import flash

from app import login_manager
from app.common.mail import send_email
from . import auth_bp
from .forms import SignupForm, LoginForm, ChangePasswordForm
from .models import Users
from app.models import Personas
from app.auth.decorators import admin_required

@auth_bp.route("/signup/", methods=["GET", "POST"])
@login_required
@admin_required
def show_signup_form():
    # if current_user.is_authenticated:
    #     return redirect(url_for('public.index'))
    form = SignupForm()
    

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        cuit = form.cuit.data
        correo_electronico = form.correo_electronico.data
        password = form.password.data
        is_admin = form.is_admin.data


        # Comprobamos que no hay ya un usuario con ese nombre de usuario
        user = Users.get_by_username(username)
        check_correo = Personas.get_by_correo(correo_electronico)
        if user is not None:
            flash ("El nombre de usuario elegido ya existe","alert-warning")
        elif check_correo and check_correo.id_usuario != None:

            flash ("Ya existe un usuario con ese correo " + check_correo.descripcion_nombre,"alert-warning")
        else:
            # Creamos el usuario y la persona relacionada al usuario y lo guardamos
            user = Users(username=username, 
                        id_estado=1, 
                        is_admin=is_admin
                        )
            user.set_password(password)
            
            #valido si la persona y si ya tiene usuario.
            check_persona = Personas.get_by_cuit(cuit)

            if check_persona and check_persona.id_usuario == None:
                user.check_persona = check_persona
                user.save()
                check_persona.id_usuario = user.id
                check_persona.save()
            elif check_persona and check_persona.id_usuario != None:
                flash("El la persona elegida ya tiene usuario.", "alert-warning")
                return redirect(url_for('admin.list_users'))
            else:
                persona = Personas(descripcion_nombre=name,
                                cuit=cuit,
                                correo_electronico=correo_electronico)
                user.persona = persona
                user.save()
            

            # Enviamos un email de bienvenida
            send_email(subject='Bienvenid@ GromaSoft',
                        sender=current_app.config['DONT_REPLY_FROM_EMAIL'],
                        recipients=[correo_electronico, ],
                        text_body=f'Hola {name}, eres nuevo usuairo de GromaSoft',
                        html_body=f'<p>Hola <strong>{name}</strong>, Ya tienes usuario en gromasoft</p>')
            # Dejamos al usuario logueado
            # login_user(user, remember=False)
            # next_page = request.args.get('next', None)
            # if not next_page or url_parse(next_page).netloc != '':
            #     next_page = url_for('public.index')
            # return redirect(next_page)
            flash("El usuario ha sido creado correctamente.", "alert-success")
            return redirect(url_for('admin.list_users'))
    return render_template("auth/signup_form.html", form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('public.index')
            return redirect(next_page)
    return render_template('auth/login_form.html', form=form)

@auth_bp.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    user = Users.get_by_username(current_user.username)
    form = ChangePasswordForm()
    if form.validate_on_submit():
        
        password_actual = user.check_password(form.password_actual.data)
        print (password_actual)
        if password_actual:
            user.set_password(form.password_nuevo.data)
            user.save()
            flash('La contraseña ha sido actualizada correctamente','alert-success')
            return redirect(url_for('public.index'))
        else:
            flash('El password actual no es correcto','alert-warning')
            
    # user = Users.get_by_username('jaltamonte')
    # user.set_password('123123')
    # user.save()
    return render_template('auth/change_password.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@login_manager.user_loader
def load_user(user_id):
    return Users.get_by_id(int(user_id))


@auth_bp.route('/firstin')
def firstin():
    #si ya está loguedo alguien significa que no corre esto y va index
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    #creamos el usuario admin que será con el que se va a poder crear un usuario válido para iniciar
    #el sistema en esta función podemos ir agregando todo lo que necesitamos que esté en la bdd y no 
    #hacer commits por fuera del sistema. 

    username = "admin"        
    user = Users.get_by_username(username)
    
    if user is not None:
        flash ("El ya fue creado","alert-warning")
        
    else:
        # Creamos el usuario admin
        user = Users(name="Admin",
                    username=username, 
                    id_estado=1, 
                    is_admin=True
                    )
        password = "Groma"
        user.set_password(password)
        
        user.save()

    
    return redirect(url_for('auth.show_signup_form'))

