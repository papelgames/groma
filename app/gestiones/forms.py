
from ast import Str
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SubmitField, TextAreaField, BooleanField, DateField,  SelectField, HiddenField, DecimalField)
from wtforms.fields import FloatField, IntegerField 
from wtforms.validators import DataRequired, Length, Email, NumberRange, ValidationError
from app.models import Personas

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

class AltaGestionesForm(FlaskForm):
    id_titular = StringField('Titular', validators=[DataRequired('Debe cargar el nombre o la razón social del titular' )])
    ubicacion_gestion= StringField('Ubicación')
    id_tipo_bienes = SelectField('Tipo de bien', choices =[], coerce = str, default = None, validators=[DataRequired('Seleccione tipo de bien')])
    fecha_inicio_gestion = DateField('Fecha de inicio de gestión')
    fecha_probable_medicion = DateField('Fecha probable de medición')
    id_tipo_gestion = SelectField('Tipo de gestión', choices =[], coerce = str, default = None, validators=[DataRequired('Seleccione tipo de gestión')])
    id_dibujante = StringField('Dibujante')
    estado_parcelario= StringField("Estado parcelario")
    numero_partida= StringField("Número de partida")
    observacion = TextAreaField('Observación', validators=[Length(max=256)])

    def validate_id_titular(self, id_titular ):
        #valido el formato de la lista de carga
        if len(id_titular.data.split('|',)) != 3:
            raise ValidationError('El titular cargado no es valido.')
        titular_x_id = Personas.get_by_id(id_titular.data.split('|',)[0])
        #valido que las personas existan en la tabla de personas. 
        if not titular_x_id:
            raise ValidationError('El titular no existe, debe crearlo.')

    def validate_id_dibujante(self, id_dibujante ):
        #valido el formato de la lista de carga
        if len(id_dibujante.data.split('|',)) != 3:
            raise ValidationError('El dibujante cargado no es valido.')
        dibujante_x_id = Personas.get_by_id(id_dibujante.data.split('|',)[0])
        #valido que las personas existan en la tabla de personas. 
        if not dibujante_x_id:
            raise ValidationError('El dibujante seleccionado no es valido.')

class ModificacionGestionesForm(AltaGestionesForm):
    fecha_medicion = DateField('Fecha de medicion')
