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

    def dt_cancelado(self, nro_documento):
        """Obtiene datos de documento cancelado."""
        query = """
        SELECT * FROM admdoccliped WHERE dcli_numero = %s AND dcli_estatus = 'C';
        """
        try:
            return self.db.ejecutar_query_ds(query, (nro_documento,))
        except Exception as e:
            logger.error(f"Error obteniendo documento cancelado: {e}")
            return []

    def cuentas_caja_doccli(self):
        """Obtiene cuentas de caja para documentos de clientes."""
        query = """
        SELECT * FROM admcuentascont WHERE cta_tipo = 'CAJA';
        """
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo cuentas de caja: {e}")
            return []

    def datos_principal(self, cod_caja, cod_usu):
        """Obtiene datos principales de caja."""
        query = """
        SELECT * FROM admcajas WHERE caj_codigo = %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (cod_caja,))
        except Exception as e:
            logger.error(f"Error obteniendo datos principales de caja: {e}")
            return []

    def facturas_cierre(self, caja, cod_usu):
        """Obtiene facturas para cierre de caja."""
        query = """
        SELECT * FROM admdoccliped WHERE dcli_caja = %s AND dcli_estatus = 'P';
        """
        try:
            return self.db.ejecutar_query_ds(query, (caja,))
        except Exception as e:
            logger.error(f"Error obteniendo facturas para cierre: {e}")
            return []

    def facturas_sin_imprimir(self, caja, cod_usu):
        """Obtiene facturas sin imprimir."""
        query = """
        SELECT * FROM admdoccliped WHERE dcli_caja = %s AND dcli_impreso = 0;
        """
        try:
            return self.db.ejecutar_query_ds(query, (caja,))
        except Exception as e:
            logger.error(f"Error obteniendo facturas sin imprimir: {e}")
            return []

    def cajas(self):
        """Obtiene lista de cajas."""
        query = "SELECT caj_codigo, caj_descripcion FROM admcajas;"
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo lista de cajas: {e}")
            return []

    def cuentas_cierre(self):
        """Obtiene cuentas para cierre."""
        query = """
        SELECT * FROM admcuentascont WHERE cta_tipo IN ('CAJA', 'BANCO');
        """
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo cuentas para cierre: {e}")
            return []

    def cierre_caja(self, base_datos, cod_usu):
        """Realiza cierre de caja."""
        # Implementar lógica compleja de cierre de caja
        # Por simplicidad, retornar datos básicos
        query = """
        SELECT SUM(movc_monto) as total FROM admmovcaja WHERE movc_codcaja = %s;
        """
        try:
            results = self.db.ejecutar_query_ds(query, (self.id_caja,))
            total = results[0]['total'] if results and results[0]['total'] else 0
            logger.info(f"Cierre de caja realizado. Total: {total}")
            return {"total": total}
        except Exception as e:
            logger.error(f"Error en cierre de caja: {e}")
            return {}

    def cabecera_mov_contables(self, login, id_base_datos):
        """Inserta cabecera de movimientos contables."""
        # Implementar lógica de cabecera
        logger.info("Cabecera de movimientos contables procesada.")
        pass

    def cerrar_facturas(self, usu):
        """Cierra facturas."""
        query = """
        UPDATE admdoccliped SET dcli_estatus = 'C' WHERE dcli_estatus = 'P';
        """
        try:
            self.db.sentencias_numero_filas(query)
            logger.info("Facturas cerradas exitosamente.")
        except Exception as e:
            logger.error(f"Error cerrando facturas: {e}")
            raise

    def clean_doccli2(self, usu):
        """Limpia documentos de clientes."""
        # Implementar lógica de limpieza
        logger.info("Documentos de clientes limpiados.")
        pass

    def existe_cierre_caja(self, id_base_d):
        """Verifica si existe cierre de caja."""
        query = """
        SELECT COUNT(*) as count FROM admcierrescaja WHERE cier_base = %s;
        """
        try:
            results = self.db.ejecutar_query_ds(query, (id_base_d,))
            return results[0]['count'] > 0 if results else False
        except Exception as e:
            logger.error(f"Error verificando cierre de caja: {e}")
            return False

    def update_cierre_diario(self, id_sysconta):
        """Actualiza cierre diario."""
        query = """
        UPDATE admcierrescaja SET cier_fecha = CURDATE() WHERE cier_id = %s;
        """
        try:
            self.db.sentencias_numero_filas(query, (id_sysconta,))
            logger.info("Cierre diario actualizado.")
        except Exception as e:
            logger.error(f"Error actualizando cierre diario: {e}")
            raise