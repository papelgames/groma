from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    correo_electronico = StringField('Correo electronico', validators=[DataRequired(), Email()])
    activo = BooleanField('activo')
    is_admin = BooleanField('administrador')
    submit = SubmitField('Registrar')
    cuit = StringField('CUIT', validators=[DataRequired(), Length(max=11)])

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
