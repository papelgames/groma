from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Length


class UserAdminForm(FlaskForm):
    is_admin = BooleanField('¿Administrador?')
    es_dibujante = BooleanField('¿Es dibujante?')
    
class PermisosUserForm(FlaskForm):
    descripcion = StringField('Nombre del permiso',validators=[DataRequired('Debe ingresar un permiso'),Length(max=256)])