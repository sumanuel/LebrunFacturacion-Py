"""
Modelos de datos para LebrunFacturacion-Py.
"""

from database import ConexionBD
from config import GLOBALES
import logging

logger = logging.getLogger(__name__)

class Compania:
    """Clase base para compañía."""
    def __init__(self):
        self.id = None
        self.nombre = None
        # Agregar más propiedades según Compania.cs

class Usuario(Compania):
    """Clase para usuarios del sistema, basada en UsuarioSistema.cs."""
    def __init__(self, db_name='db2'):  # Usar db2 (sysconf) por defecto para usuarios
        super().__init__()
        self.db = ConexionBD(db_name)
        self.id = None
        self.codigo_compania = None
        self.login = None
        self.contrasena = None
        self.mapa_menu = None
        self.numero_caja = None
        self.nombre_usuario = None
        self.ip_pc = None

    @property
    def Id(self):
        return self.id

    @Id.setter
    def Id(self, value):
        self.id = value

    @property
    def CodigoCompania(self):
        return self.codigo_compania

    @CodigoCompania.setter
    def CodigoCompania(self, value):
        self.codigo_compania = value

    @property
    def Login(self):
        return self.login

    @Login.setter
    def Login(self, value):
        self.login = value

    @property
    def Contrasena(self):
        return self.contrasena

    @Contrasena.setter
    def Contrasena(self, value):
        self.contrasena = value

    @property
    def MapaMenu(self):
        return self.mapa_menu

    @MapaMenu.setter
    def MapaMenu(self, value):
        self.mapa_menu = value

    @property
    def NumeroCaja(self):
        return self.numero_caja

    @NumeroCaja.setter
    def NumeroCaja(self, value):
        self.numero_caja = value

    @property
    def NombreUsuario(self):
        return self.nombre_usuario

    @NombreUsuario.setter
    def NombreUsuario(self, value):
        self.nombre_usuario = value

    @property
    def IpPc(self):
        return self.ip_pc

    @IpPc.setter
    def IpPc(self, value):
        self.ip_pc = value

    def validar_contrasena_parametros_c(self, password, id_database):
        """Valida contraseña en parámetros contables."""
        query = """
        SELECT pc_Descripcion FROM admparametroscontables WHERE
        (pc_ClaveComprob=%s OR pc_ClaveAsesorTributario=%s OR pc_ClaveGerenteAdministrativo=%s) AND
        pc_idSistema='08';
        """
        try:
            results = self.db.ejecutar_query_ds(query, (password, password, password))
            return len(results) > 0
        except Exception as e:
            logger.error(f"Error validando contraseña parámetros: {e}")
            return False

    def validar_usuario(self):
        """Valida usuario y contraseña."""
        query = """
        SELECT usu_mapmnu, usu_nombre, usu_codigo, usu_caja
        FROM confusuario WHERE usu_nombre=%s AND usu_clave=%s;
        """
        try:
            results = self.db.ejecutar_query_ds(query, (self.login, self.contrasena))
            if results:
                self.mapa_menu = results[0]['usu_mapmnu']
                self.id = results[0]['usu_codigo']
                self.nombre_usuario = results[0]['usu_nombre']
                self.numero_caja = results[0]['usu_caja']
                GLOBALES['Usuario_Actual'] = self.nombre_usuario  # Actualizar global
                return True
            return False
        except Exception as e:
            logger.error(f"Error validando usuario: {e}")
            return False

    def existe_usuario(self, nombre_usuario):
        """Verifica si existe un usuario."""
        query = "SELECT usu_nombre FROM confusuario WHERE usu_nombre=%s;"
        try:
            results = self.db.ejecutar_query_ds(query, (nombre_usuario,))
            return len(results) > 0
        except Exception as e:
            logger.error(f"Error verificando existencia de usuario: {e}")
            return False

    def is_clave_supervision(self, nombre_usuario, contrasena):
        """Verifica si es clave de supervisión."""
        query = "SELECT usu_fav_confirmacion FROM confusuario WHERE usu_nombre=%s AND usu_clave=%s;"
        try:
            results = self.db.ejecutar_query_ds(query, (nombre_usuario, contrasena))
            if results and results[0]['usu_fav_confirmacion'] == '1':
                return True
            return False
        except Exception as e:
            logger.error(f"Error verificando clave supervisión: {e}")
            return False

    def lbx_usuarios(self):
        """Obtiene lista de usuarios."""
        query = """
        SELECT confusuario.usu_codigo, confusuario.usu_nombre, confusuario.usu_cargo, confusuario.usu_mapmnu,
               usu_compania, usu_administracion FROM confusuario
        LEFT JOIN confusuario2 ON confusuario.usu_codigo = confusuario2.usu_codigo LIMIT 100;
        """
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo lista de usuarios: {e}")
            return []

    def buscar_usuarios(self, filtro, tipo_busqueda):
        """Busca usuarios por filtro."""
        if tipo_busqueda == "codigo":
            condition = "confusuario.usu_codigo LIKE %s"
        elif tipo_busqueda == "descripcion":
            condition = "usu_nombre LIKE %s"
        else:
            return []

        query = f"""
        SELECT confusuario.usu_codigo, confusuario.usu_nombre, confusuario.usu_cargo, confusuario.usu_mapmnu,
               usu_compania, usu_administracion FROM confusuario
        LEFT JOIN confusuario2 ON confusuario.usu_codigo = confusuario2.usu_codigo
        WHERE {condition};
        """
        try:
            return self.db.ejecutar_query_ds(query, (f"%{filtro}%",))
        except Exception as e:
            logger.error(f"Error buscando usuarios: {e}")
            return []