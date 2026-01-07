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

    def armar_data_table_mov_contab(self):
        """Arma la estructura del DataTable para movimientos contables."""
        columns = [
            "item", "codprove", "numeroDoc", "sufiDoc", "tipoDoc", "numComprobante", "descripcion",
            "cuenta", "tipo", "baseTipo", "fecha", "hora", "monto", "status", "login", "idSistemas",
            "auxiliar", "rif", "nombre", "tipoLetra", "islr", "interno", "referencia"
        ]
        self.tabla_contabilidad = pd.DataFrame(columns=columns)
        return self.tabla_contabilidad