
import datetime
from email.policy import default
from itertools import product
from types import ClassMethodDescriptorType
from typing import Text

from slugify import slugify
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth.models import Users

from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                     onupdate=db.func.current_timestamp())

class Personas (Base):
    __tablename__ = "personas"
    descripcion_nombre = db.Column(db.String(50), nullable = False)
    cuit = db.Column(db.String(11), nullable = False)
    correo_electronico = db.Column(db.String(256))
    telefono = db.Column(db.String(256))
    tipo_persona = db.Column(db.String(50))
    id_estado = db.Column(db.Integer)
    nota = db.Column(db.String(256))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Personas.query.all()
    
    @staticmethod
    def get_by_id(id_persona):
        return Personas.query.filter_by(id = id_persona).first()
    
    @staticmethod
    def get_by_cuit(cuit):
        return Personas.query.filter_by(cuit = cuit).first()
    
    @staticmethod
    def get_like_descripcion_all_paginated(descripcion_, page=1, per_page=20):
        descripcion_ = descripcion_.replace(' ','%')
        return db.session.query(Personas)\
            .filter(Personas.descripcion_nombre.contains(descripcion_))\
            .paginate(page=page, per_page=per_page, error_out=False)
    

class Gestiones (Base):
    __tablename__ = "gestiones"
    id_cliente = db.Column(db.Integer)
    id_titular = db.Column(db.Integer)
    ubicacion_gestion= db.Column(db.String(50))
    fecha_inicio_gestion = db.Column(db.DateTime)
    fecha_medicion = db.Column(db.DateTime)
    fecha_probable_inicio = db.Column(db.DateTime)
    fecha_asignacion_dibujante = db.Column(db.DateTime)
    fecha_devolucion_dibujante = db.Column(db.DateTime)
    fecha_fin_gestion = db.Column(db.DateTime)
    id_dibujante = db.Column(db.Integer)
    id_tipo_gestion = db.Column(db.Integer)
    id_estado = db.Column(db.Integer)
    estado_parcelario= db.Column(db.String(50))
    numero_partida= db.Column(db.String(50))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Cobros (Base):
    __tablename__ = "cobros"
    fecha_probable_cobro = db.Column(db.DateTime, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, nullable = False)
    importe_total = db.Column(db.Numeric(precision=15, scale=2))
    estado = db.Column(db.Integer)
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class ImportesCobros (Base):
    __tablename__ = "importescobros"
    id_cobro = db.Column(db.Integer, nullable = False)
    fecha_cobro = db.Column(db.DateTime, nullable = False)
    importe = db.Column(db.Numeric(precision=15, scale=2))
    tipo_cambio = db.Column(db.Numeric(precision=15, scale=2))
    moneda = db.Column(db.String(25))
    medio_cobro = db.Column(db.String(25))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Observaciones (Base):
    __tablename__ = "observaciones"
    id_gestion = db.Column(db.Integer)
    id_cobro = db.Column(db.Integer)
    id_importe_cobro = db.Column(db.Integer)
    observacion = db.Column(db.String(256))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Estados(Base):
    __tablename__ = "estados"
    descripcion = db.Column(db.String(50))
    tabla = db.Column(db.String(50))
    inicial = db.Column(db.Boolean)
    final = db.Column(db.Boolean)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class TiposGestiones(Base):
    __tablename__ = "tiposgestiones"
    descripcion = db.Column(db.String(50))
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()