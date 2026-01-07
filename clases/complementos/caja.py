"""
Módulo para la clase Caja.
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from clasesData.database import ConexionBD
import logging

logger = logging.getLogger(__name__)

class Caja:
    """Clase para gestionar caja, basada en Caja.cs (versión simplificada)."""

    def __init__(self):
        self.db = ConexionBD('db1')  # sisadm
        self.db_sysconta = ConexionBD('db3')  # sysconta
        self.correlativo_caja = None
        self.total_facturas = 0.0
        self.total_devolucion = 0.0
        self.total_cuadre = 0.0
        self.total_efectivo = 0.0
        self.total_cheque = 0.0
        self.total_tdebito = 0.0
        self.total_tcredito = 0.0
        self.total_iva = 0.0
        self.id_caja = None
        # Agregar más atributos según necesidad

    # Propiedades principales
    @property
    def TotalFacturas(self):
        return self.total_facturas

    @TotalFacturas.setter
    def TotalFacturas(self, value):
        self.total_facturas = value

    @property
    def TotalEfectivo(self):
        return self.total_efectivo

    @TotalEfectivo.setter
    def TotalEfectivo(self, value):
        self.total_efectivo = value

    @property
    def IdCaja(self):
        return self.id_caja

    @IdCaja.setter
    def IdCaja(self, value):
        self.id_caja = value

    def insert_mov_caja_facturacion(self, datos, factura_relacionada):
        """Inserta movimientos de caja para facturación (versión simplificada)."""
        query = """
        INSERT INTO admmovcaja (movc_numtra, movc_codmaestr, movc_numdoc, movc_descrioper,
        movc_operacion, mocv_forpag, movc_codtipopag, movc_tipoctaban, movc_cuentacheq,
        movc_numero, movc_monto, movc_divisa, movc_fchemision, movc_hora, movc_vendedor,
        movc_codcaja, movc_tipomovc, movc_estatus, movc_valcam, movc_memo)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            # Obtener correlativo
            correlativo = self.obtener_correlativo_movcaja()
            fecha = datetime.now().strftime('%Y-%m-%d')
            hora = datetime.now().strftime('%H:%M:%S')

            # Asumir datos es una lista de diccionarios
            for fila in datos:
                self.db.sentencias_numero_filas(query, (
                    correlativo, fila.get('codmaestr'), fila.get('numdoc'), fila.get('descrioper'),
                    fila.get('operacion'), fila.get('forpag'), fila.get('codtipopag'), fila.get('tipoctaban'),
                    fila.get('cuentacheq'), fila.get('numero'), fila.get('monto'), fila.get('divisa'),
                    fecha, hora, fila.get('vendedor'), self.id_caja, fila.get('tipomovc'),
                    fila.get('estatus'), fila.get('valcam'), fila.get('memo')
                ))
                correlativo = str(int(correlativo) + 1).zfill(10)  # Incrementar correlativo
            logger.info("Movimientos de caja insertados exitosamente.")
        except Exception as e:
            logger.error(f"Error insertando movimientos de caja: {e}")
            raise

    def obtener_correlativo_movcaja(self):
        """Obtiene el correlativo para movimientos de caja."""
        query = "SELECT MAX(movc_numtra) FROM admmovcaja;"
        try:
            results = self.db.ejecutar_query_ds(query)
            if results and results[0]['MAX(movc_numtra)']:
                return str(int(results[0]['MAX(movc_numtra)']) + 1).zfill(10)
            return "0000000001"
        except Exception as e:
            logger.error(f"Error obteniendo correlativo: {e}")
            return "0000000001"

    # Agregar más métodos según necesidad (cierre de caja, reportes, etc.)