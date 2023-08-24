
from ast import Str
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, DateField,  SelectField, HiddenField, DecimalField)
from wtforms.fields import FloatField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class BusquedaForm(FlaskForm):
    buscar = StringField('Buscar')

class AltaPersonasForm(FlaskForm):
    descripcion_nombre = StringField("Nombre/Razón Social", validators=[DataRequired('Debe cargar el nombre o la razón social' )])
    correo_electronico = StringField('Correo electrónico', validators=[Email()])
    telefono = StringField('Telefono')
    cuit = StringField('CUIT', validators=[DataRequired(), Length(max=11)])
    tipo_persona = SelectField('Tipo de persona', choices =[( '','Seleccionar acción'),( "fisica",'Persona Física'),( "juridica",'Persona Jurídica')], coerce = str, default = None, validators=[DataRequired('Seleccione tipo de persona')])
    #estado = SelectField('Tipo de persona', choices =[], coerce = str, default = None)
    nota = TextAreaField('Nota', validators=[Length(max=256)])

class ProductosPresupuestoForm(FlaskForm):
    buscar = StringField('Buscar')
    id = IntegerField()
    descripcion = StringField()
    cantidad = IntegerField()
    importe = FloatField()
    condicion = StringField()
    registro = StringField()
