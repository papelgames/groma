# from tarfile import PAX_NUMBER_FIELDS
# from threading import activeCount
from flask_login import UserMixin
# from jinja2 import PrefixLoader
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    id_estado = db.Column(db.Integer)

    # def __init__(self, name, email):
    #     self.name = name
    #     self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Users.query.get(id)

    @staticmethod
    def get_by_username(username):
        return Users.query.filter_by(username=username).first()

    @staticmethod
    def get_all():
        return Users.query.all()
    
    # @staticmethod
    # def get_by_perfil_activo(perfil):
    #     return User.query.filter_by(activo=True, perfil = perfil).all()
