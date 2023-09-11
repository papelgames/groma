from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError


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
    password = PasswordField('Password', validators=[DataRequired('Debe ingresar una contraseña')])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    password_actual = PasswordField('Password actual', validators=[DataRequired('Debe completar el password')])
    password_nuevo = PasswordField('Password nuevo', validators=[DataRequired('Debe completar un password')])
    password_nuevo_re = PasswordField('Confirma Password ')

    def validate_password_nuevo_re (self, password_nuevo_re):
        print(password_nuevo_re)
        print(self.password_nuevo.data)
        if password_nuevo_re.data != self.password_nuevo.data:
            raise ValidationError('El password no coincide')

class ForgetPasswordForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired('Debe completar el usuario'), Length(max=15)])

class FindUserForm(FlaskForm):
    correo_electronico = StringField('Correo electronico', validators=[DataRequired('Debe completar el correo electronico'), Email()])