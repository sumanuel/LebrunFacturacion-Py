"""
Modelos de datos para LebrunFacturacion-Py.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .database import ConexionBD
from config import GLOBALES
import logging

logger = logging.getLogger(__name__)

class Compania:
    """Clase para compañías, basada en Compania.cs."""
    def __init__(self, compania_conectar=None):
        self.db = ConexionBD('db2')  # sysconf
        self.nombre = None
        self.direccion = None
        self.rif = None
        self.codigo = None
        self.base_datos_actual = None
        self.base_datos_compania = None
        self.minister = None
        self.sso = None
        self.telf = None
        self.fax = None
        self.telf1 = None
        self.pagina = None
        self.tipper = None
        self.contribuyente = None
        self.moneda = None
        self.moneetxt = None
        self.cajain = None
        self.mdcv = None
        self.invcxs = None
        self.cpsd = None
        self.compania_conectar = compania_conectar

    # Propiedades con getters/setters
    @property
    def Nombre(self):
        return self.nombre

    @Nombre.setter
    def Nombre(self, value):
        self.nombre = value

    @property
    def Rif(self):
        return self.rif

    @Rif.setter
    def Rif(self, value):
        self.rif = value

    @property
    def Codigo(self):
        return self.codigo

    @Codigo.setter
    def Codigo(self, value):
        self.codigo = value

    @property
    def BaseDatosActual(self):
        return self.base_datos_actual

    @BaseDatosActual.setter
    def BaseDatosActual(self, value):
        self.base_datos_actual = value

    @property
    def BaseDatosCompania(self):
        return self.base_datos_compania

    @BaseDatosCompania.setter
    def BaseDatosCompania(self, value):
        self.base_datos_compania = value

    @property
    def Direccion(self):
        return self.direccion

    @Direccion.setter
    def Direccion(self, value):
        self.direccion = value

    # Más propiedades...
    @property
    def Invcxs(self):
        return self.invcxs

    @Invcxs.setter
    def Invcxs(self, value):
        self.invcxs = value

    @property
    def Cpsd(self):
        return self.cpsd

    @Cpsd.setter
    def Cpsd(self, value):
        self.cpsd = value

    @property
    def Mdcv(self):
        return self.mdcv

    @Mdcv.setter
    def Mdcv(self, value):
        self.mdcv = value

    @property
    def Cajain(self):
        return self.cajain

    @Cajain.setter
    def Cajain(self, value):
        self.cajain = value

    @property
    def Moneetxt(self):
        return self.moneetxt

    @Moneetxt.setter
    def Moneetxt(self, value):
        self.moneetxt = value

    @property
    def Moneda(self):
        return self.moneda

    @Moneda.setter
    def Moneda(self, value):
        self.moneda = value

    @property
    def Contribuyente(self):
        return self.contribuyente

    @Contribuyente.setter
    def Contribuyente(self, value):
        self.contribuyente = value

    @property
    def Tipper(self):
        return self.tipper

    @Tipper.setter
    def Tipper(self, value):
        self.tipper = value

    @property
    def Pagina(self):
        return self.pagina

    @Pagina.setter
    def Pagina(self, value):
        self.pagina = value

    @property
    def Telf1(self):
        return self.telf1

    @Telf1.setter
    def Telf1(self, value):
        self.telf1 = value

    @property
    def Fax(self):
        return self.fax

    @Fax.setter
    def Fax(self, value):
        self.fax = value

    @property
    def Telf(self):
        return self.telf

    @Telf.setter
    def Telf(self, value):
        self.telf = value

    @property
    def Sso(self):
        return self.sso

    @Sso.setter
    def Sso(self, value):
        self.sso = value

    @property
    def Minister(self):
        return self.minister

    @Minister.setter
    def Minister(self, value):
        self.minister = value

    @property
    def CompaniaConectar(self):
        return self.compania_conectar

    @CompaniaConectar.setter
    def CompaniaConectar(self, value):
        self.compania_conectar = value

    def obtener_companias(self):
        """Obtiene lista de compañías."""
        query = "SELECT empre_nombre, empre_codigo, empre_actual FROM confdatosempresa;"
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo compañías: {e}")
            return []

    def obtener_codigo_compania_actual(self):
        """Obtiene el código de la compañía actual."""
        query = "SELECT empre_codigo, empre_nombre, empre_rif FROM confdatosempresa WHERE empre_actual = 1;"
        try:
            results = self.db.ejecutar_query_ds(query)
            if results:
                self.codigo = results[0]['empre_codigo']
                self.base_datos_compania = results[0]['empre_codigo']
                self.base_datos_actual = results[0]['empre_codigo']
                # Obtener datos adicionales de admconfisisten
                query2 = "SELECT * FROM admconfisisten;"
                self.db.modificar_conexion_string(1)  # Cambiar a db1
                results2 = self.db.ejecutar_query_ds(query2)
                if results2:
                    row = results2[0]
                    self.nombre = row.get('confi_nombre')
                    self.direccion = row.get('confi_direcc')
                    self.rif = row.get('confi_rif')
                    self.minister = row.get('confi_minister')
                    self.sso = row.get('confi_sso')
                    self.telf = row.get('confi_telefono')
                    self.fax = row.get('confi_fax')
                    self.telf1 = row.get('confi_tel1')
                    self.pagina = row.get('confi_pagina')
                    self.tipper = row.get('confi_tipper')
                    self.contribuyente = row.get('confi_contribuy')
                    # Más campos si es necesario
        except Exception as e:
            logger.error(f"Error obteniendo código compañía actual: {e}")

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