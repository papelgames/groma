
import datetime
from email.policy import default
from itertools import product
from types import ClassMethodDescriptorType
from typing import Text

from slugify import slugify
from sqlalchemy import func, or_, alias, not_
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
#from app.auth.models import Users

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
    def get_by_correo(correo):
        return Personas.query.filter_by(correo_electronico = correo).first()
        
    @staticmethod
    def get_like_descripcion_all_paginated(descripcion_, page=1, per_page=20):
        descripcion_ = descripcion_.replace(' ','%')
        return db.session.query(Personas)\
            .filter(Personas.descripcion_nombre.contains(descripcion_))\
            .paginate(page=page, per_page=per_page, error_out=False)

personas_cliente = aliased(Personas)
personas_dibujante = aliased(Personas)

class Gestiones (Base):
    __tablename__ = "gestiones"
    id_cliente = db.Column(db.Integer)
    titular = db.Column(db.String(50), nullable = False)
    ubicacion_gestion= db.Column(db.String(50))
    coordenadas=db.Column(db.String(50))
    fecha_inicio_gestion = db.Column(db.DateTime)
    fecha_probable_medicion = db.Column(db.DateTime)
    fecha_medicion = db.Column(db.DateTime)
    fecha_asignacion_dibujante = db.Column(db.DateTime)
    fecha_devolucion_dibujante = db.Column(db.DateTime)
    fecha_fin_gestion = db.Column(db.DateTime)
    id_dibujante = db.Column(db.Integer)
    id_analista_responsable = db.Column(db.Integer)
    id_tipo_gestion = db.Column(db.Integer)
    id_tipo_bienes = db.Column(db.Integer)
    id_estado = db.Column(db.Integer)
    numero_partido= db.Column(db.String(4))
    numero_partida= db.Column(db.String(8))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))
    observaciones = db.relationship('Observaciones', backref='gestiones', uselist=True, lazy=True)
    tareas = db.relationship('Tareas', secondary='gestionesportareas', back_populates='gestiones')
     
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(page=1, per_page=20):
        return db.session.query(Gestiones, personas_cliente, personas_dibujante, TiposGestiones, TiposBienes)\
            .filter(Gestiones.id_cliente == personas_cliente.id)\
            .filter(Gestiones.id_dibujante == personas_dibujante.id)\
            .filter(Gestiones.id_tipo_gestion == TiposGestiones.id)\
            .filter(Gestiones.id_tipo_bienes == TiposBienes.id)\
            .paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_id(id_):
        return db.session.query(Gestiones, personas_cliente, personas_dibujante, TiposGestiones, TiposBienes)\
            .filter(Gestiones.id_cliente == personas_cliente.id)\
            .filter(Gestiones.id_dibujante == personas_dibujante.id)\
            .filter(Gestiones.id_tipo_gestion == TiposGestiones.id)\
            .filter(Gestiones.id_tipo_bienes == TiposBienes.id)\
            .filter(Gestiones.id == id_)\
            .first()
    
    @staticmethod
    def get_first_by_id(id):
        return Gestiones.query.filter_by(id = id).first()
        
    @staticmethod
    def get_like_descripcion_all_paginated(descripcion_, page=1, per_page=20):
        descripcion_ = descripcion_.replace(' ','%')
        return db.session.query(Gestiones, personas_cliente, personas_dibujante, TiposGestiones, TiposBienes)\
            .filter(Gestiones.id_cliente == personas_cliente.id)\
            .filter(Gestiones.id_dibujante == personas_dibujante.id)\
            .filter(Gestiones.id_tipo_gestion == TiposGestiones.id)\
            .filter(Gestiones.id_tipo_bienes == TiposBienes.id)\
            .filter(personas_cliente.descripcion_nombre.contains(descripcion_))\
            .paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_gestiones_by_id_cliente_all_paginated(id_cliente_, page=1, per_page=20):
        return db.session.query(Gestiones, personas_cliente, personas_dibujante, TiposGestiones)\
            .filter(Gestiones.id_cliente == personas_cliente.id)\
            .filter(Gestiones.id_dibujante == personas_dibujante.id)\
            .filter(Gestiones.id_tipo_gestion == TiposGestiones.id)\
            .filter(Gestiones.id_cliente == id_cliente_)\
            .paginate(page=page, per_page=per_page, error_out=False)

class Cobros (Base):
    __tablename__ = "cobros"
    id_gestion = db.Column(db.Integer, nullable = False)
    fecha_probable_cobro = db.Column(db.DateTime, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, nullable = False)
    importe_total = db.Column(db.Numeric(precision=15, scale=2))
    moneda = db.Column(db.String(25))
    estado = db.Column(db.Integer)
    limitada = db.Column(db.Boolean)
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))
    observaciones = db.relationship('Observaciones', backref='cobros', uselist=False)
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Cobros.query.all()
    
    @staticmethod
    def get_all_by_id_gestion(id_gestion):
        return Cobros.query.filter_by(id_gestion = id_gestion).first()
    
    @staticmethod
    def get_all_by_id_cobro(id_cobro):
        return Cobros.query.filter_by(id = id_cobro).first()

    @staticmethod
    def get_by_id(id_persona):
        return Cobros.query.filter_by(id = id_persona).first()
    
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
    observaciones = db.relationship('Observaciones', backref='importe_cobro', uselist=False)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Observaciones (Base):
    __tablename__ = "observaciones"
    id_gestion = db.Column(db.Integer, db.ForeignKey('gestiones.id'))
    id_cobro = db.Column(db.Integer, db.ForeignKey('cobros.id'))
    id_importe_cobro = db.Column(db.Integer, db.ForeignKey('importescobros.id'))
    id_detalle_gxt = db.Column(db.Integer, db.ForeignKey('detallesgxt.id'))
    observacion = db.Column(db.String(256))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all_by_id_gestion(id_gestion):
        return Observaciones.query.filter_by(id_gestion = id_gestion).all()

class Estados(Base):
    __tablename__ = "estados"
    clave = db.Column(db.Integer)
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
    limitada = db.Column(db.Boolean)
    tareas = db.relationship('Tareas', secondary='tiposgestionesportareas', back_populates='tipos_gestiones')
    
    @staticmethod
    def get_all():
        return TiposGestiones.query.all()

    @staticmethod
    def get_all_by_id(id_tipo_gestion):
        return TiposGestiones.query.filter_by(id = id_tipo_gestion).all()
    
    @staticmethod
    def get_first_by_id(id_tipo_gestion):
        return TiposGestiones.query.filter_by(id = id_tipo_gestion).first()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class TiposBienes(Base):
    __tablename__ = "tiposbienes"
    descripcion = db.Column(db.String(50))
    
    @staticmethod
    def get_all():
        return TiposBienes.query.all()
        
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class PermisosPorUsuarios(Base):
    __tablename__ = "permisosporusuarios"
    id_permiso = db.Column(db.Integer, db.ForeignKey('permisos.id'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id'))

class Roles(Base):
    __tablename__ = "roles"
    descripcion = db.Column(db.String(50))
    id_permiso = db.Column(db.Integer, db.ForeignKey('permisos.id'))
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def get_all_by_id(id_rol):
        return Roles.query.filter_by(id = id_rol).first()

    @staticmethod
    def get_all_by_descripcion(descripcion):
        return Roles.query.filter_by(descripcion = descripcion).all()

    @staticmethod
    def get_all_descripcion_agrupada():
        return db.session.query(Roles.descripcion.label('nombre_rol')).distinct().all()

class Permisos(Base):
    __tablename__ = "permisos"
    descripcion = db.Column(db.String(50))
    roles = db.relationship('Roles', backref='permisos', uselist=True, lazy=True)
    users = db.relationship('Users', secondary='permisosporusuarios', back_populates='permisos')
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_all():
        return Permisos.query.all()

    @staticmethod
    def get_by_id(id_permiso):
        return Permisos.query.filter_by(id = id_permiso).first()
    
class GestionesPorTareas(Base):
    __tablename__ = "gestionesportareas"
    id_gestion = db.Column(db.Integer, db.ForeignKey('gestiones.id'))
    id_tarea = db.Column(db.Integer, db.ForeignKey('tareas.id'))
    detallesgxt = db.relationship('DetallesGxT', backref='gestionesportareas', uselist=False)

class DetallesGxT(Base):
    __tablename__ = "detallesgxt"
    id_gestion_por_tarea =db.Column(db.Integer, db.ForeignKey('gestionesportareas.id'))
    fecha_inicio = db.Column(db.DateTime)
    fecha_fin = db.Column(db.DateTime)
    fecha_vencimiento = db.Column(db.DateTime)
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))
    observaciones = db.relationship('Observaciones', backref='detallesgxt', uselist=True, lazy=True)
    
class Tareas(Base):
    __tablename__ = "tareas"
    descripcion = db.Column(db.String(50))
    correlativa_de = db.Column(db.Integer)
    dias_para_vencimiento = db.Column(db.Integer)
    usuario_alta = db.Column(db.String(256))
    usuario_modificacion = db.Column(db.String(256))
    fecha_unica = db.Column(db.Boolean)
    gestiones = db.relationship('Gestiones', secondary='gestionesportareas', back_populates='tareas')
    tipos_gestiones = db.relationship('TiposGestiones', secondary='tiposgestionesportareas', back_populates='tareas')

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Tareas.query.all()
    
    @staticmethod
    def get_first_by_id(id_tarea):
        return Tareas.query.filter_by(id = id_tarea).first()

    @staticmethod
    def get_tareas_no_relacionadas(id_gestion): 
        return  Tareas.query.filter(~Tareas.gestiones.any(id=id_gestion)).all()
    
class TiposGestionesPorTareas(Base):
    __tablename__ = "tiposgestionesportareas"
    id_tipo_gestion = db.Column(db.Integer, db.ForeignKey('tiposgestiones.id'))
    id_tarea = db.Column(db.Integer, db.ForeignKey('tareas.id'))
