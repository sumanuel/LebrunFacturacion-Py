"""
Módulo para la clase Banco.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from clasesData.database import ConexionBD
import logging

logger = logging.getLogger(__name__)

class Banco:
    """Clase para gestionar bancos, basada en Banco.cs."""

    def __init__(self):
        self.db = ConexionBD('db1')  # Usar db1 (sisadm) para bancos
        self.cod_banco = None
        self.nombre_banco = None
        self.direccion_banco = None
        self.telf1 = None
        self.telf2 = None
        self.status = None
        self.pagina_web = None
        self.login = None
        self.clave = None
        self.casillero = None
        self.memo = None
        self.ultimo_cod = None

    # Propiedades
    @property
    def CodBanco(self):
        return self.cod_banco

    @CodBanco.setter
    def CodBanco(self, value):
        self.cod_banco = value

    @property
    def NombreBanco(self):
        return self.nombre_banco

    @NombreBanco.setter
    def NombreBanco(self, value):
        self.nombre_banco = value

    @property
    def DireccionBanco(self):
        return self.direccion_banco

    @DireccionBanco.setter
    def DireccionBanco(self, value):
        self.direccion_banco = value

    @property
    def Telf1(self):
        return self.telf1

    @Telf1.setter
    def Telf1(self, value):
        self.telf1 = value

    @property
    def Telf2(self):
        return self.telf2

    @Telf2.setter
    def Telf2(self, value):
        self.telf2 = value

    @property
    def Status(self):
        return self.status

    @Status.setter
    def Status(self, value):
        self.status = value

    @property
    def PaginaWeb(self):
        return self.pagina_web

    @PaginaWeb.setter
    def PaginaWeb(self, value):
        self.pagina_web = value

    @property
    def Login(self):
        return self.login

    @Login.setter
    def Login(self, value):
        self.login = value

    @property
    def Clave(self):
        return self.clave

    @Clave.setter
    def Clave(self, value):
        self.clave = value

    @property
    def Casillero(self):
        return self.casillero

    @Casillero.setter
    def Casillero(self, value):
        self.casillero = value

    @property
    def Memo(self):
        return self.memo

    @Memo.setter
    def Memo(self, value):
        self.memo = value

    def lbx_bancos(self):
        """Obtiene lista de bancos para listbox."""
        query = "SELECT ban_codigo, ban_nombre, ban_tel3 FROM admbancos LIMIT 200;"
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo lista de bancos: {e}")
            return []

    def limpiar_datos_banco(self):
        """Limpia los datos del banco."""
        self.cod_banco = None
        self.nombre_banco = None

    def buscar_bancos_cod_nom(self, cod_banco):
        """Busca bancos por código o nombre."""
        query = """
        SELECT ban_codigo, ban_nombre, ban_tel3 FROM admbancos
        WHERE ban_codigo LIKE %s OR ban_nombre LIKE %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (f"%{cod_banco}%", f"%{cod_banco}%"))
        except Exception as e:
            logger.error(f"Error buscando bancos: {e}")
            return []

    def registrar_banco(self):
        """Registra un nuevo banco."""
        query = """
        INSERT INTO admbancos (ban_codigo, ban_nombre, ban_direccion, ban_tel1, ban_tel2,
        ban_tel3, ban_pagina, ban_login, ban_clave, ban_casillero, ban_memo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            self.db.sentencias_numero_filas(query, (
                self.cod_banco, self.nombre_banco, self.direccion_banco, self.telf1,
                self.telf2, self.status, self.pagina_web, self.login, self.clave,
                self.casillero, self.memo
            ))
            logger.info(f"Banco {self.cod_banco} registrado exitosamente.")
        except Exception as e:
            logger.error(f"Error registrando banco: {e}")
            raise

    def actualizar_banco(self, num_banco):
        """Actualiza un banco existente."""
        query = """
        UPDATE admbancos SET ban_nombre=%s, ban_direccion=%s, ban_tel1=%s, ban_tel2=%s,
        ban_tel3=%s, ban_pagina=%s, ban_login=%s, ban_clave=%s, ban_casillero=%s,
        ban_memo=%s WHERE ban_codigo=%s;
        """
        try:
            self.db.sentencias_numero_filas(query, (
                self.nombre_banco, self.direccion_banco, self.telf1, self.telf2,
                self.status, self.pagina_web, self.login, self.clave, self.casillero,
                self.memo, num_banco
            ))
            logger.info(f"Banco {num_banco} actualizado exitosamente.")
        except Exception as e:
            logger.error(f"Error actualizando banco: {e}")
            raise

    def armar_datos_banco(self, num_banco):
        """Obtiene datos de un banco específico."""
        query = """
        SELECT ban_codigo, ban_nombre, ban_direccion, ban_tel1, ban_tel2,
        ban_tel3, ban_pagina, ban_login, ban_clave, ban_casillero, ban_memo
        FROM admbancos WHERE ban_codigo=%s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (num_banco,))
        except Exception as e:
            logger.error(f"Error obteniendo datos del banco {num_banco}: {e}")
            return []

    def obtener_ultimo_cod(self):
        """Obtiene el último código de banco."""
        query = "SELECT ban_codigo FROM admbancos ORDER BY ban_codigo DESC LIMIT 1;"
        try:
            results = self.db.ejecutar_query_ds(query)
            if results:
                self.ultimo_cod = results[0]['ban_codigo']
                return self.ultimo_cod
            return None
        except Exception as e:
            logger.error(f"Error obteniendo último código: {e}")
            return None