from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

db = SQLAlchemy()

class UsuarioSistema(UserMixin, db.Model):
    """Modelo para usuarios del sistema"""
    __tablename__ = 'confusuarios'

    id = db.Column('usu_codigo', db.Integer, primary_key=True)
    login = db.Column('usu_login', db.String(50), unique=True, nullable=False)
    password_hash = db.Column('usu_password', db.String(255), nullable=False)
    nombre = db.Column('usu_nombre', db.String(100))
    activo = db.Column('usu_activo', db.Boolean, default=True)
    mapa_menu = db.Column('usu_mapamenu', db.String(10))
    ultimo_acceso = db.Column('usu_ultimoacceso', db.DateTime)
    intentos_fallidos = db.Column('usu_intentosfallidos', db.Integer, default=0)

    # Relaciones
    permisos_compania = db.relationship('PermisoCompania', backref='usuario', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.activo

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<UsuarioSistema {self.login}>'

class Compania(db.Model):
    """Modelo para compañías/empresas"""
    __tablename__ = 'confdatosempresa'

    codigo = db.Column('empre_codigo', db.String(10), primary_key=True)
    nombre = db.Column('empre_nombre', db.String(100), nullable=False)
    rif = db.Column('empre_rif', db.String(20))
    activo = db.Column('empre_actual', db.Boolean, default=True)

    # Relaciones
    permisos = db.relationship('PermisoCompania', backref='compania', lazy=True)

    def __repr__(self):
        return f'<Compania {self.nombre}>'

class PermisoCompania(db.Model):
    """Modelo para permisos de usuario por compañía"""
    __tablename__ = 'confpermisoscompania'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column('usu_codigo', db.Integer, db.ForeignKey('confusuarios.usu_codigo'), nullable=False)
    compania_codigo = db.Column('empre_codigo', db.String(10), db.ForeignKey('confdatosempresa.empre_codigo'), nullable=False)
    activo = db.Column('perm_activo', db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint('usu_codigo', 'empre_codigo', name='unique_usuario_compania'),
    )

    def __repr__(self):
        return f'<PermisoCompania usuario={self.usuario_id} compania={self.compania_codigo}>'

class MenuItem(db.Model):
    """Modelo para items del menú"""
    __tablename__ = 'conf_menu'

    id = db.Column('menu_id', db.Integer, primary_key=True)
    padre = db.Column('menu_padre', db.String(50), nullable=False)
    subpadre = db.Column('menu_subpadre', db.String(50))
    hijo = db.Column('menu_hijo', db.String(50))
    ruta = db.Column('menu_ruta', db.String(255))
    nombre = db.Column('menu_nombre', db.String(100))
    icono = db.Column('menu_icono', db.String(50))
    orden = db.Column('menu_orden', db.Integer, default=0)
    activo = db.Column('menu_activo', db.Boolean, default=True)

    def __repr__(self):
        return f'<MenuItem {self.padre}.{self.subpadre}.{self.hijo}>'

class MapaMenu(db.Model):
    """Modelo para mapas de menú por usuario"""
    __tablename__ = 'confmapamenu'

    id = db.Column('mmn_id', db.Integer, primary_key=True)
    codigo = db.Column('mmn_codigo', db.String(10), nullable=False)
    modulo = db.Column('mmn_modulo', db.String(50), nullable=False)
    menu_antiguo = db.Column('mmn_menu', db.String(50))
    formulario = db.Column('mmn_formulario', db.String(255))
    activo = db.Column('mmn_activo', db.Boolean, default=True)

    def __repr__(self):
        return f'<MapaMenu {self.modulo}:{self.menu_antiguo}>'

class SesionUsuario(db.Model):
    """Modelo para controlar sesiones de usuario"""
    __tablename__ = 'conf_sesiones'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('confusuarios.usu_codigo'), nullable=False)
    token_sesion = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    fecha_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_fin = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True)

    usuario = db.relationship('UsuarioSistema', backref=db.backref('sesiones', lazy=True))

    def __repr__(self):
        return f'<SesionUsuario usuario={self.usuario_id} activo={self.activo}>'