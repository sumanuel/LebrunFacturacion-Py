"""
Módulo para la clase MovimientoContable.
"""

import sys
import os
from datetime import datetime
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from clasesData.database import ConexionBD
import logging

logger = logging.getLogger(__name__)

class MovimientoContable:
    """Clase para gestionar movimientos contables, basada en movimientoContable.cs."""

    def __init__(self):
        self.db = ConexionBD('db3')  # sysconta
        self.numero_comprobante = None
        self.tabla_contabilidad = pd.DataFrame()
        self.cabecera_tabla_conta = pd.DataFrame()

    @property
    def TablaContabilidad(self):
        return self.tabla_contabilidad

    @TablaContabilidad.setter
    def TablaContabilidad(self, value):
        self.tabla_contabilidad = value

    @property
    def CabeceraTablaConta(self):
        return self.cabecera_tabla_conta

    @CabeceraTablaConta.setter
    def CabeceraTablaConta(self, value):
        self.cabecera_tabla_conta = value

    def obtener_numero_comprobante(self, bd, pc_id_sistemas):
        """Obtiene el número de comprobante y lo incrementa."""
        query = "SELECT pc_idSistema, pc_CorrCompAut + 1 FROM admparametroscontables WHERE pc_idSistema = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (pc_id_sistemas,))
            if results:
                # Incrementar el correlativo
                update_query = "UPDATE admparametroscontables SET pc_CorrCompAut = pc_CorrCompAut + 1 WHERE pc_idSistema = %s;"
                self.db.sentencias_numero_filas(update_query, (pc_id_sistemas,))
                return results
            return []
        except Exception as e:
            logger.error(f"Error obteniendo número de comprobante: {e}")
            return []

    def ingresar_mov_contab(self, tabla_mov_contab):
        """Ingresa movimientos contables."""
        query = """
        INSERT INTO admmovcontab (movcon_item, movcon_proveedor, movcon_numdoc, movcon_sufdoc,
        movcon_tipdoc, movcon_numcomp, movcon_descrip, movcon_cuenta, movcon_tipo, movcon_basetip,
        movcon_fecaha, movcon_hora, movcon_monto, movcon_status, movcon_login, idSistemas,
        movcon_auxiliar, movcon_rif, movcon_nombre, codigoIslr, referencia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            # Asumir tabla_mov_contab es DataFrame o lista de diccionarios
            for _, row in tabla_mov_contab.iterrows():
                self.db.sentencias_numero_filas(query, (
                    row['item'], row['codprove'], row['numeroDoc'], row['sufiDoc'], row['tipoDoc'],
                    row['numComprobante'], row['descripcion'], row['cuenta'], row['tipo'], row['baseTipo'],
                    row['fecha'], row['hora'], row['monto'], '1', row['login'], row['idSistemas'],
                    row['auxiliar'], row['rif'], row['nombre'], row['islr'], row['referencia']
                ))
            logger.info("Movimientos contables insertados exitosamente.")
        except Exception as e:
            logger.error(f"Error insertando movimientos contables: {e}")
            raise

    def cabecera_syscontab(self, tabla_mov_contab, compania):
        """Inserta cabecera en syscontab."""
        query = """
        INSERT INTO admmovimientoscontablesc (mc_nroComprobante, mc_FechaComprobante, mc_FechaCarga,
        mc_FechaCierre, mc_IdSistema, mc_Descripcion, mc_MontoDebitos, mc_MontoCreditos, mc_Status,
        mc_Login, mc_LoginUpd, mc_FechaUltMod, mc_Compania, mc_HoraGuardado, IdSistemas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')
            for _, row in tabla_mov_contab.iterrows():
                self.db.sentencias_numero_filas(query, (
                    row['comprobante'], fecha, fecha, fecha, row['mcIdSistema'], row['descripcion'],
                    row['Debito'], row['Credito'], '2', row['login'], row['updateLogin'],
                    fecha, compania, hora, row['idSistema']
                ))
            logger.info("Cabecera syscontab insertada exitosamente.")
        except Exception as e:
            logger.error(f"Error insertando cabecera syscontab: {e}")
            raise

    def detalles_syscontab(self, tabla_mov_contab, compania):
        """Inserta detalles en syscontab."""
        query = """
        INSERT INTO admmovimientoscontablesd (md_nroComprobante, md_Item, md_Cuenta, md_Auxiliar,
        md_Tipo, md_Monto, md_Referencia, md_IdSistema, md_Compania)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            for _, row in tabla_mov_contab.iterrows():
                self.db.sentencias_numero_filas(query, (
                    row['comprobante'], row['item'], row['cuenta'], row['auxiliar'],
                    row['tipo'], row['monto'], row['referencia'], row['idSistema'], compania
                ))
            logger.info("Detalles syscontab insertados exitosamente.")
        except Exception as e:
            logger.error(f"Error insertando detalles syscontab: {e}")
            raise

    def armar_data_table_mov_contab(self):
        """Arma la estructura del DataTable para movimientos contables."""
        columns = [
            "item", "codprove", "numeroDoc", "sufiDoc", "tipoDoc", "numComprobante", "descripcion",
            "cuenta", "tipo", "baseTipo", "fecha", "hora", "monto", "status", "login", "idSistemas",
            "auxiliar", "rif", "nombre", "tipoLetra", "islr", "interno", "referencia"
        ]
        self.tabla_contabilidad = pd.DataFrame(columns=columns)
        return self.tabla_contabilidad

    def armar_data_table_cabecera_mov_contab(self):
        """Arma la estructura del DataTable para cabecera de movimientos contables."""
        columns = [
            "comprobante", "mcIdSistema", "descripcion", "Debito", "Credito", "login", "updateLogin", "idSistema"
        ]
        self.cabecera_tabla_conta = pd.DataFrame(columns=columns)
        return self.cabecera_tabla_conta

    def cuenta_doc(self, tipo_doc):
        """Obtiene cuenta por tipo de documento."""
        query = "SELECT * FROM admcuentascont WHERE cta_tipodoc = %s;"
        try:
            return self.db.ejecutar_query_ds(query, (tipo_doc,))
        except Exception as e:
            logger.error(f"Error obteniendo cuenta por documento: {e}")
            return []

    def cuenta_cliente(self, cod_cliente):
        """Obtiene cuenta contable del cliente."""
        query = "SELECT cli_cuentamanor, cli_auxiliar FROM admclientes WHERE cli_codigo = %s;"
        try:
            return self.db.ejecutar_query_ds(query, (cod_cliente,))
        except Exception as e:
            logger.error(f"Error obteniendo cuenta del cliente: {e}")
            return []

    def datos_comprobante(self, comprobante, compania, cliente=None):
        """Obtiene datos de comprobante."""
        if cliente:
            query = """
            SELECT * FROM admmovcontab WHERE movcon_numcomp = %s AND movcon_proveedor = %s;
            """
            params = (comprobante, cliente)
        else:
            query = """
            SELECT * FROM admmovcontab WHERE movcon_numcomp = %s;
            """
            params = (comprobante,)
        try:
            return self.db.ejecutar_query_ds(query, params)
        except Exception as e:
            logger.error(f"Error obteniendo datos de comprobante: {e}")
            return []

    def reimprimir_comprobante(self, comprobante, compania):
        """Reimprime comprobante."""
        # Implementar lógica de reimpresión
        logger.info(f"Comprobante {comprobante} preparado para reimpresión.")
        return self.datos_comprobante(comprobante, compania)

    def reimprimir_comprobante_syscontab(self, comprobante, compania):
        """Reimprime comprobante desde syscontab."""
        query = """
        SELECT * FROM admmovimientoscontablesc WHERE mc_nroComprobante = %s AND mc_Compania = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (comprobante, compania))
        except Exception as e:
            logger.error(f"Error reimprimiendo comprobante syscontab: {e}")
            return []

    def armar_data_table_cabecera_mov_contab2(self):
        """Arma segunda estructura de cabecera."""
        return self.armar_data_table_cabecera_mov_contab()

    def cuenta_tip_doc_pro2(self, tipo_doc, codigo_cliente):
        """Obtiene cuenta por tipo de documento y cliente."""
        query = """
        SELECT * FROM admcuentascont WHERE cta_tipodoc = %s AND cta_cliente = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (tipo_doc, codigo_cliente))
        except Exception as e:
            logger.error(f"Error obteniendo cuenta por tipo y cliente: {e}")
            return []

    def cuenta_idb(self, codigo):
        """Obtiene cuenta por IDB."""
        query = "SELECT * FROM admcuentascont WHERE cta_idb = %s;"
        try:
            return self.db.ejecutar_query_ds(query, (codigo,))
        except Exception as e:
            logger.error(f"Error obteniendo cuenta IDB: {e}")
            return []

    def reimprimir_comprobante(self, comprobante, compania, id_sistema):
        """Reimprime comprobante con ID de sistema."""
        query = """
        SELECT * FROM admmovcontab WHERE movcon_numcomp = %s AND idSistemas = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (comprobante, id_sistema))
        except Exception as e:
            logger.error(f"Error reimprimiendo comprobante con ID sistema: {e}")
            return []

    def cabecera_syscontab_status(self, tabla_mov_contab, compania):
        """Inserta cabecera con status."""
        # Similar a cabecera_syscontab pero con status específico
        self.cabecera_syscontab(tabla_mov_contab, compania)

    def detalles_syscontab_status(self, tabla_mov_contab, compania):
        """Inserta detalles con status."""
        # Similar a detalles_syscontab
        self.detalles_syscontab(tabla_mov_contab, compania)

    def eliminar_mov_contab(self, proveedor, docum, suf, tipo):
        """Elimina movimiento contable."""
        query = """
        DELETE FROM admmovcontab WHERE movcon_proveedor = %s AND movcon_numdoc = %s
        AND movcon_sufdoc = %s AND movcon_tipdoc = %s;
        """
        try:
            self.db.sentencias_numero_filas(query, (proveedor, docum, suf, tipo))
            logger.info("Movimiento contable eliminado.")
        except Exception as e:
            logger.error(f"Error eliminando movimiento contable: {e}")
            raise

    def ingresar_mov_contab_temp(self, tabla_mov_contab):
        """Ingresa movimientos contables temporales."""
        # Similar a ingresar_mov_contab pero en tabla temporal
        temp_table = "admmovcontab_temp"
        query = f"""
        INSERT INTO {temp_table} (movcon_item, movcon_proveedor, movcon_numdoc, movcon_sufdoc,
        movcon_tipdoc, movcon_numcomp, movcon_descrip, movcon_cuenta, movcon_tipo, movcon_basetip,
        movcon_fecaha, movcon_hora, movcon_monto, movcon_status, movcon_login, idSistemas,
        movcon_auxiliar, movcon_rif, movcon_nombre, codigoIslr, referencia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            for _, row in tabla_mov_contab.iterrows():
                self.db.sentencias_numero_filas(query, (
                    row['item'], row['codprove'], row['numeroDoc'], row['sufiDoc'], row['tipoDoc'],
                    row['numComprobante'], row['descripcion'], row['cuenta'], row['tipo'], row['baseTipo'],
                    row['fecha'], row['hora'], row['monto'], '1', row['login'], row['idSistemas'],
                    row['auxiliar'], row['rif'], row['nombre'], row['islr'], row['referencia']
                ))
            logger.info("Movimientos contables temporales insertados.")
        except Exception as e:
            logger.error(f"Error insertando movimientos temporales: {e}")
            raise

    def comproba_contable_compras(self, tipo_doc, codigo, docum, sufijo):
        """Obtiene comprobante contable de compras."""
        query = """
        SELECT * FROM admmovcontab WHERE movcon_tipdoc = %s AND movcon_proveedor = %s
        AND movcon_numdoc = %s AND movcon_sufdoc = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (tipo_doc, codigo, docum, sufijo))
        except Exception as e:
            logger.error(f"Error obteniendo comprobante de compras: {e}")
            return []