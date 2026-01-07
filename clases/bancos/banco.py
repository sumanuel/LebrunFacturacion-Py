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

    def cargar_lbx_cuentas_banc(self):
        """Carga lista de cuentas bancarias para listbox."""
        query = """
        SELECT ctas_banco 'Codigo', ctas_nomban 'Banco', ctas_tirular 'Titular',
        ctas_tipo 'Cuenta', ctas_numero 'Numero Cuenta', ctas_divisa 'Divisa',
        ctas_sucursal 'Sucursal', ctas_activa 'Activa' FROM admcuentasbanc;
        """
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error cargando cuentas bancarias: {e}")
            return []

    def busqueda_cuenta_banc(self, opcion, busqueda):
        """Busca cuentas bancarias según opción."""
        if opcion == 0:
            query = """
            SELECT ctas_banco 'Codigo', ctas_nomban 'Banco', ctas_tirular 'Titular',
            ctas_tipo 'Cuenta', ctas_numero 'Numero Cuenta', ctas_divisa 'Divisa',
            ctas_sucursal 'Sucursal', ctas_activa 'Activa' FROM admcuentasbanc;
            """
            params = ()
        elif opcion == 1:
            query = """
            SELECT ctas_banco 'Codigo', ctas_nomban 'Banco', ctas_tirular 'Titular',
            ctas_tipo 'Cuenta', ctas_numero 'Numero Cuenta', ctas_divisa 'Divisa',
            ctas_sucursal 'Sucursal', ctas_activa 'Activa' FROM admcuentasbanc
            WHERE ctas_nomban = %s;
            """
            params = (busqueda,)
        elif opcion == 2:
            query = """
            SELECT ctas_banco 'Codigo', ctas_nomban 'Banco', ctas_tirular 'Titular',
            ctas_tipo 'Cuenta', ctas_numero 'Numero Cuenta', ctas_divisa 'Divisa',
            ctas_sucursal 'Sucursal', ctas_activa 'Activa' FROM admcuentasbanc
            WHERE ctas_numero = %s;
            """
            params = (busqueda,)
        else:
            return []

        try:
            return self.db.ejecutar_query_ds(query, params)
        except Exception as e:
            logger.error(f"Error buscando cuentas bancarias: {e}")
            return []

    def insertar_nueva_cuenta_banc(self, tabla, ide):
        """Inserta una nueva cuenta bancaria."""
        # Implementar lógica de inserción basada en DataTable
        # Por simplicidad, asumir que tabla es una lista de dicts
        for row in tabla:
            query = """
            INSERT INTO admcuentasbanc (ctas_banco, ctas_nomban, ctas_tirular, ctas_tipo,
            ctas_numero, ctas_divisa, ctas_sucursal, ctas_activa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            try:
                self.db.sentencias_numero_filas(query, (
                    row.get('ctas_banco'), row.get('ctas_nomban'), row.get('ctas_tirular'),
                    row.get('ctas_tipo'), row.get('ctas_numero'), row.get('ctas_divisa'),
                    row.get('ctas_sucursal'), row.get('ctas_activa')
                ))
            except Exception as e:
                logger.error(f"Error insertando cuenta bancaria: {e}")
                raise

    def eliminar_cuenta_bancaria(self, codigo_banco, titular, numero_cuenta):
        """Elimina una cuenta bancaria."""
        query = """
        DELETE FROM admcuentasbanc WHERE ctas_banco = %s AND ctas_tirular = %s AND ctas_numero = %s;
        """
        try:
            self.db.sentencias_numero_filas(query, (codigo_banco, titular, numero_cuenta))
            logger.info(f"Cuenta bancaria {numero_cuenta} eliminada.")
        except Exception as e:
            logger.error(f"Error eliminando cuenta bancaria: {e}")
            raise

    def armar_modificacion(self, codigo_banco, titular, tipo_cuenta, numero_cuenta):
        """Arma datos para modificación de cuenta bancaria."""
        query = """
        SELECT * FROM admcuentasbanc WHERE ctas_banco = %s AND ctas_tirular = %s
        AND ctas_tipo = %s AND ctas_numero = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (codigo_banco, titular, tipo_cuenta, numero_cuenta))
        except Exception as e:
            logger.error(f"Error obteniendo datos para modificación: {e}")
            return []

    def modificar_cuenta_banc(self, tabla, ide):
        """Modifica una cuenta bancaria."""
        # Similar a insertar, pero UPDATE
        for row in tabla:
            query = """
            UPDATE admcuentasbanc SET ctas_nomban = %s, ctas_tirular = %s, ctas_tipo = %s,
            ctas_numero = %s, ctas_divisa = %s, ctas_sucursal = %s, ctas_activa = %s
            WHERE ctas_banco = %s;
            """
            try:
                self.db.sentencias_numero_filas(query, (
                    row.get('ctas_nomban'), row.get('ctas_tirular'), row.get('ctas_tipo'),
                    row.get('ctas_numero'), row.get('ctas_divisa'), row.get('ctas_sucursal'),
                    row.get('ctas_activa'), row.get('ctas_banco')
                ))
            except Exception as e:
                logger.error(f"Error modificando cuenta bancaria: {e}")
                raise

    def obtener_numeros_cuenta(self, codigo_ban):
        """Obtiene números de cuenta para un banco."""
        query = "SELECT ctas_numero FROM admcuentasbanc WHERE ctas_banco = %s;"
        try:
            return self.db.ejecutar_query_ds(query, (codigo_ban,))
        except Exception as e:
            logger.error(f"Error obteniendo números de cuenta: {e}")
            return []

    def obtener_datos_chequera(self, codigo_banco, numero_cuenta):
        """Obtiene datos de chequera."""
        query = """
        SELECT * FROM admchequeras WHERE cheq_banco = %s AND cheq_numero = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (codigo_banco, numero_cuenta))
        except Exception as e:
            logger.error(f"Error obteniendo datos de chequera: {e}")
            return []

    def reactivar_chequera(self, codigo_banco, numero_cuenta, chequera):
        """Reactiva una chequera."""
        query = """
        UPDATE admchequeras SET cheq_activa = 1 WHERE cheq_banco = %s AND cheq_numero = %s AND cheq_chequera = %s;
        """
        try:
            self.db.sentencias_numero_filas(query, (codigo_banco, numero_cuenta, chequera))
            logger.info(f"Chequera {chequera} reactivada.")
        except Exception as e:
            logger.error(f"Error reactivando chequera: {e}")
            raise

    def actualizar_ultimo_cheque(self, codigo_banco, numero_cuenta, chequera, numero_cheque):
        """Actualiza el último número de cheque."""
        query = """
        UPDATE admchequeras SET cheq_ultimo = %s WHERE cheq_banco = %s AND cheq_numero = %s AND cheq_chequera = %s;
        """
        try:
            self.db.sentencias_numero_filas(query, (numero_cheque, codigo_banco, numero_cuenta, chequera))
            logger.info(f"Último cheque actualizado a {numero_cheque}.")
        except Exception as e:
            logger.error(f"Error actualizando último cheque: {e}")
            raise

    def obtener_cuenta_contable_banco(self, codigo_banco, cuenta_banc=None):
        """Obtiene cuenta contable del banco."""
        if cuenta_banc:
            query = """
            SELECT * FROM admcuentascont WHERE cta_banco = %s AND cta_cuentabanc = %s;
            """
            params = (codigo_banco, cuenta_banc)
        else:
            query = """
            SELECT * FROM admcuentascont WHERE cta_banco = %s;
            """
            params = (codigo_banco,)
        try:
            return self.db.ejecutar_query_ds(query, params)
        except Exception as e:
            logger.error(f"Error obteniendo cuenta contable: {e}")
            return []