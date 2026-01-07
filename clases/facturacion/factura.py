import os
import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any, List
import pandas as pd

logger = logging.getLogger(__name__)

class Factura:
    """
    Clase que representa una factura en el sistema de facturación.
    Equivalente a la clase Factura.cs del proyecto original.
    """

    def __init__(self, timeout: Optional[int] = None, tipo: Optional[str] = None, ip: Optional[str] = None):
        # Importar aquí para evitar importaciones circulares
        from clasesData.database import ConexionBD
        from clases.clientes import Clientes
        from clases.vendedores import Vendedor

        # Conexión a base de datos
        if timeout:
            self.database = ConexionBD('db1', timeout)  # sisadm
        else:
            self.database = ConexionBD('db1')  # sisadm

        # Atributos principales
        self.base_gn: Decimal = Decimal('0')
        self.base_ex: Decimal = Decimal('0')
        self.base_rd: Decimal = Decimal('0')
        self.iva_gn: Decimal = Decimal('0')
        self.iva_rd: Decimal = Decimal('0')
        self.iva_total: Decimal = Decimal('0')
        self.total_neto: Decimal = Decimal('0')
        self.total_base: Decimal = Decimal('0')
        self.descuento_items: Decimal = Decimal('0')
        self.costo_nacional: Decimal = Decimal('0')
        self.costo_importado: Decimal = Decimal('0')
        self.base_nacional: Decimal = Decimal('0')
        self.base_importada: Decimal = Decimal('0')

        # Strings
        self.factura_afectada: str = ""
        self.numero_fiscal_afectado: str = ""
        self.hora_afectada: str = ""
        self.fecha_afectada: str = ""
        self.eoc_afectado: str = ""
        self.correlativo_interno: str = ""
        self.tipo_documento: str = tipo or ""
        self.condicion: str = ""
        self.divisa: str = ""
        self.numero_fiscal: str = ""
        self.modelo_impresora: str = ""
        self.serie_impresora: str = ""
        self.dcli_aprob1: str = ""
        self.dcli_aprob2: str = ""
        self.dcli_aprob3: str = ""
        self.dcli_estado: str = ""
        self.dcli_expexp: str = ""
        self.ctd_codcta: str = ""
        self.numero_pedido: str = ""
        self.direccion_envio: str = ""
        self.dir_obra: str = ""
        self.certificado: str = ""
        self.nombre_reporte: str = ""
        self.peso: str = ""
        self.bultos: str = ""
        self.estatus: str = ""
        self.dias_pp1: str = ""
        self.dias_pp2: str = ""
        self.porcentaje_pp1: str = ""
        self.porcentaje_pp2: str = ""
        self.codigo_rechazo: str = ""
        self.dcli_anufis: str = ""

        # Fechas
        self.fecha_factura: datetime = datetime.now()

        # Números
        self.descuento_general: Decimal = Decimal('0')
        self.plazo_dias: int = 0
        self.total_items: int = 0
        self.maxima_cantidad_detalles: int = 0

        # Objetos relacionados
        self.cliente_facturar: Optional[Clientes] = None
        self.vendedor_factura: Optional[Vendedor] = None
        self.dgv_items: Optional[pd.DataFrame] = None

        # Inicializar objetos si se pasaron parámetros
        if tipo and ip:
            self.obtener_modelo_fiscal(ip)
            self.get_factura_afectada()

        # Inicializar aprobaciones
        self.dcli_aprob1 = ""
        self.dcli_aprob2 = ""
        self.dcli_aprob3 = ""

        # Inicializar vendedor
        self.vendedor_factura = Vendedor()

    def obtener_modelo_fiscal(self, ip: str) -> None:
        """Obtiene el modelo fiscal de la impresora."""
        query = "SELECT ctd_serief FROM admtipdoccli WHERE ctd_tipo = %s;"
        try:
            results = self.database.ejecutar_query_ds(query, (self.tipo_documento,))
            if results:
                self.serie_impresora = results[0]['ctd_serief']
        except Exception as e:
            logger.error(f"Error obteniendo modelo fiscal: {e}")

    def get_factura_afectada(self) -> None:
        """Obtiene la factura afectada."""
        # Implementar lógica según el tipo de documento
        pass

    def lbx_fact(self, caja: str) -> List[dict]:
        """Obtiene lista de facturas para listbox."""
        query = """
        SELECT dcli_numero, dcli_codigo, cli_nombre, dcli_fecha, dcli_estado, dcli_neto,
               dcli_tiptra, dcli_baseneta, dcli_numfis, dcli_impreso, dcli_tipdoc, dcli_codmon, dcli_facafe
        FROM admdoccli2
        LEFT OUTER JOIN admclientes ON admclientes.cli_codigo = admdoccli2.dcli_codigo
        WHERE dcli_tipdoc = 'FAV' AND dcli_caja = %s AND dcli_cerrado != '1'
        GROUP BY dcli_codigo, dcli_numero
        ORDER BY dcli_numero DESC, dcli_codigo ASC LIMIT 100;
        """
        try:
            return self.database.ejecutar_query_ds(query, (caja,))
        except Exception as e:
            logger.error(f"Error obteniendo lista de facturas: {e}")
            return []

    def lbx_dev(self, caja: str) -> List[dict]:
        """Obtiene lista de notas de crédito para listbox."""
        query = """
        SELECT dcli_numero, dcli_codigo, cli_nombre, dcli_fecha, dcli_estado, dcli_neto,
               dcli_tiptra, dcli_baseneta, dcli_numfis, dcli_impreso, dcli_tipdoc, dcli_codmon, dcli_facafe
        FROM admdoccli2
        LEFT OUTER JOIN admclientes ON admclientes.cli_codigo = admdoccli2.dcli_codigo
        WHERE dcli_tipdoc = 'DEV' AND dcli_caja = %s AND dcli_cerrado != '1'
        GROUP BY dcli_codigo, dcli_numero
        ORDER BY dcli_numero DESC, dcli_codigo ASC LIMIT 100;
        """
        try:
            return self.database.ejecutar_query_ds(query, (caja,))
        except Exception as e:
            logger.error(f"Error obteniendo lista de notas de crédito: {e}")
            return []

    def lbx_nde(self, caja: str) -> List[dict]:
        """Obtiene lista de notas de débito para listbox."""
        query = """
        SELECT dcli_numero, dcli_codigo, cli_nombre, dcli_fecha, dcli_estado, dcli_neto,
               dcli_tiptra, dcli_baseneta, dcli_numfis, dcli_impreso, dcli_tipdoc, dcli_codmon, dcli_facafe
        FROM admdoccli2
        LEFT OUTER JOIN admclientes ON admclientes.cli_codigo = admdoccli2.dcli_codigo
        WHERE dcli_tipdoc = 'NDE' AND dcli_caja = %s AND dcli_cerrado != '1'
        GROUP BY dcli_codigo, dcli_numero
        ORDER BY dcli_numero DESC, dcli_codigo ASC LIMIT 100;
        """
        try:
            return self.database.ejecutar_query_ds(query, (caja,))
        except Exception as e:
            logger.error(f"Error obteniendo lista de notas de débito: {e}")
            return []

    def factura_buscada(self, numero: str, tipo_documento: str) -> List[dict]:
        """Busca facturas por número o fiscal."""
        query = """
        SELECT dcli_numero, dcli_codigo, cli_nombre, dcli_fecha, dcli_estado, dcli_neto,
               dcli_tiptra, dcli_baseneta, dcli_numfis, dcli_impreso, dcli_tipdoc, dcli_codmon, dcli_facafe
        FROM admdoccli
        LEFT JOIN admclientes ON admclientes.cli_codigo = admdoccli.dcli_codigo
        WHERE (dcli_numero LIKE %s OR dcli_numfis LIKE %s OR admclientes.cli_nombre LIKE %s) AND dcli_tipdoc = %s;
        """
        search_term = f"%{numero}%"
        try:
            return self.database.ejecutar_query_ds(query, (search_term, search_term, search_term, tipo_documento))
        except Exception as e:
            logger.error(f"Error buscando factura: {e}")
            return []

    def factura_buscada2(self, fecha1: str, fecha2: str, tipo_doc: str) -> List[dict]:
        """Busca facturas por rango de fechas."""
        query = """
        SELECT dcli_numero, dcli_codigo, cli_nombre, dcli_fecha, dcli_estado, dcli_neto,
               dcli_tiptra, dcli_baseneta, dcli_numfis, dcli_impreso, dcli_tipdoc, dcli_codmon, dcli_facafe
        FROM admdoccli
        LEFT JOIN admclientes ON admclientes.cli_codigo = admdoccli.dcli_codigo
        WHERE dcli_fecha BETWEEN %s AND %s AND dcli_tipdoc = %s;
        """
        try:
            return self.database.ejecutar_query_ds(query, (fecha1, fecha2, tipo_doc))
        except Exception as e:
            logger.error(f"Error buscando facturas por fecha: {e}")
            return []

    def obtener_correlativo(self, tipo_doc: str) -> str:
        """Obtiene el correlativo para un tipo de documento."""
        query = "SELECT ctd_correlativo FROM admtipdoccli WHERE ctd_tipo = %s;"
        try:
            results = self.database.ejecutar_query_ds(query, (tipo_doc,))
            if results:
                correlativo = str(int(float(results[0]['ctd_correlativo'])) + 1).zfill(12)
                self.correlativo_interno = correlativo
                return correlativo
            return ""
        except Exception as e:
            logger.error(f"Error obteniendo correlativo: {e}")
            return ""

    def acumular_bases(self, precio: Decimal, iva: str) -> None:
        """Acumula bases según el tipo de IVA."""
        if iva == "EX":
            self.base_ex += precio
        elif iva == "GN":
            self.base_gn += precio
        elif iva == "RD":
            self.base_rd += precio

    def restar_bases(self, precio: Decimal, iva: str) -> None:
        """Resta bases según el tipo de IVA."""
        if iva == "EX":
            self.base_ex -= precio
        elif iva == "GN":
            self.base_gn -= precio
        elif iva == "RD":
            self.base_rd -= precio

    def acumular_ivas(self, precio: Decimal, iva: str) -> None:
        """Acumula IVAs según el tipo."""
        query = "SELECT alict_venta FROM admiva WHERE alict_tipodiva = %s;"
        try:
            results = self.database.ejecutar_query_ds(query, (iva,))
            if results:
                valor_venta = 1 + (Decimal(str(results[0]['alict_venta'])) / 100)
                iva_acumular = ((precio * valor_venta) - precio).quantize(Decimal('0.01'))

                if iva == "GN":
                    self.iva_gn = iva_acumular
                    self.iva_total = self.iva_gn + self.iva_rd
                elif iva == "RD":
                    self.iva_rd = iva_acumular
                    self.iva_total = self.iva_gn + self.iva_rd
                elif iva == "A":
                    self.iva_rd = iva_acumular
                    self.iva_total = self.iva_gn + self.iva_rd
        except Exception as e:
            logger.error(f"Error acumulando IVAs: {e}")

    def restar_ivas(self, precio: Decimal, iva: str) -> None:
        """Resta IVAs según el tipo."""
        query = "SELECT alict_venta FROM admiva WHERE alict_tipodiva = %s;"
        try:
            results = self.database.ejecutar_query_ds(query, (iva,))
            if results:
                valor_venta = 1 + (Decimal(str(results[0]['alict_venta'])) / 100)
                iva_acumular = ((precio * valor_venta) - precio).quantize(Decimal('0.01'))

                if iva == "GN":
                    self.iva_gn -= iva_acumular
                    self.iva_total = self.iva_gn + self.iva_rd
                elif iva == "RD":
                    self.iva_rd -= iva_acumular
                    self.iva_total = self.iva_gn + self.iva_rd
                elif iva == "A":
                    self.iva_rd -= iva_acumular
                    self.iva_total = self.iva_gn + self.iva_rd
        except Exception as e:
            logger.error(f"Error restando IVAs: {e}")

    def aumentar_correlativo(self, tipo_doc: str, numero: str) -> None:
        """Aumenta el correlativo en la base de datos."""
        query = "SELECT ctd_correlativo FROM admtipdoccli WHERE ctd_tipo = %s;"
        try:
            results = self.database.ejecutar_query_ds(query, (tipo_doc,))
            if results:
                temp_correlativo = float(results[0]['ctd_correlativo'])
                resta = temp_correlativo - float(numero)

                if resta < 0:
                    update_query = "UPDATE admtipdoccli SET ctd_correlativo = %s WHERE ctd_tipo = %s;"
                    new_correlativo = str(temp_correlativo + abs(resta)).zfill(12)
                    self.database.sentencias_numero_filas(update_query, (new_correlativo, tipo_doc))
                elif resta == 0:
                    update_query = "UPDATE admtipdoccli SET ctd_correlativo = %s WHERE ctd_tipo = %s;"
                    new_correlativo = str(float(numero) + 1).zfill(12)
                    self.database.sentencias_numero_filas(update_query, (new_correlativo, tipo_doc))
                elif resta > 0:
                    update_query = "UPDATE admtipdoccli SET ctd_correlativo = %s WHERE ctd_tipo = %s;"
                    new_correlativo = str(float(numero) + resta).zfill(12)
                    self.database.sentencias_numero_filas(update_query, (new_correlativo, tipo_doc))
        except Exception as e:
            logger.error(f"Error aumentando correlativo: {e}")

    def tiene_pp(self, fact: 'Factura') -> bool:
        """
        Verifica si la factura tiene pronto pago configurado.
        """
        if fact.dias_pp1 and fact.dias_pp1.strip():
            try:
                if int(fact.dias_pp1) > 0:
                    return True
            except ValueError:
                pass
        return False

    # Propiedades calculadas (equivalentes a los getters/setters)
    @property
    def base_gn_prop(self) -> Decimal:
        return self.base_gn

    @base_gn_prop.setter
    def base_gn_prop(self, value: Decimal):
        self.base_gn = value

    @property
    def iva_total_prop(self) -> Decimal:
        return self.iva_total

    @iva_total_prop.setter
    def iva_total_prop(self, value: Decimal):
        self.iva_total = value

    @property
    def total_neto_prop(self) -> Decimal:
        return self.total_neto

    @total_neto_prop.setter
    def total_neto_prop(self, value: Decimal):
        self.total_neto = value

    @property
    def total_base_prop(self) -> Decimal:
        return self.total_base

    @total_base_prop.setter
    def total_base_prop(self, value: Decimal):
        self.total_base = value

    @property
    def correlativo_interno_prop(self) -> str:
        return self.correlativo_interno

    @correlativo_interno_prop.setter
    def correlativo_interno_prop(self, value: str):
        self.correlativo_interno = value

    @property
    def tipo_documento_prop(self) -> str:
        return self.tipo_documento

    @tipo_documento_prop.setter
    def tipo_documento_prop(self, value: str):
        self.tipo_documento = value

    @property
    def cliente_facturar_prop(self) -> Optional[Any]:
        return self.cliente_facturar

    @cliente_facturar_prop.setter
    def cliente_facturar_prop(self, value: Optional[Any]):
        self.cliente_facturar = value

    @property
    def vendedor_factura_prop(self) -> Optional[Any]:
        return self.vendedor_factura

    @vendedor_factura_prop.setter
    def vendedor_factura_prop(self, value: Optional[Any]):
        self.vendedor_factura = value

    @property
    def numero_fiscal_prop(self) -> str:
        return self.numero_fiscal

    @numero_fiscal_prop.setter
    def numero_fiscal_prop(self, value: str):
        self.numero_fiscal = value

    @property
    def numero_pedido_prop(self) -> str:
        return self.numero_pedido

    @numero_pedido_prop.setter
    def numero_pedido_prop(self, value: str):
        self.numero_pedido = value

    @property
    def direccion_envio_prop(self) -> str:
        return self.direccion_envio

    @direccion_envio_prop.setter
    def direccion_envio_prop(self, value: str):
        self.direccion_envio = value

    @property
    def peso_prop(self) -> str:
        return self.peso

    @peso_prop.setter
    def peso_prop(self, value: str):
        self.peso = value

    @property
    def bultos_prop(self) -> str:
        return self.bultos

    @bultos_prop.setter
    def bultos_prop(self, value: str):
        self.bultos = value

    @property
    def dias_pp1_prop(self) -> str:
        return self.dias_pp1

    @dias_pp1_prop.setter
    def dias_pp1_prop(self, value: str):
        self.dias_pp1 = value

    @property
    def porcentaje_pp1_prop(self) -> str:
        return self.porcentaje_pp1

    @porcentaje_pp1_prop.setter
    def porcentaje_pp1_prop(self, value: str):
        self.porcentaje_pp1 = value

    @property
    def dias_pp2_prop(self) -> str:
        return self.dias_pp2

    @dias_pp2_prop.setter
    def dias_pp2_prop(self, value: str):
        self.dias_pp2 = value

    @property
    def porcentaje_pp2_prop(self) -> str:
        return self.porcentaje_pp2

    @porcentaje_pp2_prop.setter
    def porcentaje_pp2_prop(self, value: str):
        self.porcentaje_pp2 = value

    def cargarFactura(self, numeroInter: str, clientF: 'Clientes', vend1: 'Vendedor') -> None:
        """Carga una factura existente desde la base de datos."""
        query = """
        SELECT dcli_codigo, dcli_codmon, dcli_codven, dcli_condic, dcli_facafe,
               dcli_tipafe, dcli_tipdoc, dcli_invmon, dcli_baseneta, dcli_descitem,
               dcli_subbase, doc_impo, TRUNCATE(dcli_cantproduc, 0) as dcli_cantproduc,
               dcli_cosfac_n, dcli_cosfac_i, dcli_base_n, dcli_base_i, dcli_saldo,
               dcli_subtotal, dcli_ivaRD, dcli_ivaGN, dcli_estado
        FROM admdoccli WHERE dcli_numero = %s;
        """
        try:
            results = self.database.ejecutar_query_ds(query, (numeroInter,))
            if results:
                row = results[0]
                clientF.Codigo = row['dcli_codigo']
                self.divisa = row['dcli_codmon']
                vend1.CodigoV = row['dcli_codven']
                clientF.CondicionPago = row['dcli_condic']
                self.correlativo_interno = numeroInter
                self.factura_afectada = row['dcli_facafe']
                self.tipo_documento = row['dcli_tipdoc']
                self.divisa = row['dcli_invmon']
                self.total_base = Decimal(str(row['dcli_baseneta']).replace(',', '.'))
                self.descuento_items = Decimal(str(row['dcli_descitem']).replace(',', '.'))
                self.base_ex = Decimal(str(row['dcli_subbase']).replace(',', '.'))
                self.base_gn = Decimal(str(row['doc_impo']).replace(',', '.'))
                self.total_items = int(float(row['dcli_cantproduc']))
                self.costo_nacional = Decimal(str(row['dcli_cosfac_n']).replace(',', '.'))
                self.costo_importado = Decimal(str(row['dcli_cosfac_i']).replace(',', '.'))
                self.base_nacional = Decimal(str(row['dcli_base_n']).replace(',', '.'))
                self.base_importada = Decimal(str(row['dcli_base_i']).replace(',', '.'))
                self.total_neto = Decimal(str(row['dcli_saldo']).replace(',', '.'))
                self.total_base = Decimal(str(row['dcli_subtotal']).replace(',', '.'))
                self.iva_rd = Decimal(str(row['dcli_ivaRD']).replace(',', '.'))
                self.iva_gn = Decimal(str(row['dcli_ivaGN']).replace(',', '.'))
                self.dcli_estado = row['dcli_estado']
        except Exception as e:
            logger.error(f"Error cargando factura: {e}")

    def guardarDetalleFac(self, detalles: pd.DataFrame) -> None:
        """Guarda los detalles de la factura."""
        # Implementar lógica para guardar detalles
        # Esta es una versión simplificada, necesitaría más parámetros según el código C#
        pass

    def crearSentenciaCabecera(self, clienteFactura: 'Clientes', vendedorFactura: 'Vendedor',
                              codigoEmpresaActual: str, codigoUsuario: str, codCaja: str,
                              cambio: str, pagado: str, contado: str) -> str:
        """Crea la sentencia SQL para insertar la cabecera de la factura."""
        # Implementar la creación de la sentencia SQL compleja
        # Esta es una versión simplificada
        sql = """
        INSERT INTO admdoccli (
            dcli_cbtnum, dcli_cencos, dcli_codigo, dcli_codmon, dcli_sucursal,
            dcli_transpo, dcli_codven, dcli_condic, dcli_destino, dcli_origen,
            dcli_estado, dcli_expexp, dcli_facafe, dcli_girnum, dcli_hora,
            dcli_modfis, dcli_numero, dcli_numfis, dcli_numgtr, dcli_plaexp,
            dcli_recnum, dcli_serfis, dcli_succli, dcli_tipafe, dcli_tipdoc,
            dcli_tiptra, dcli_usuario, dcli_zona, dcli_fecharecep, dcli_fchven,
            dcli_fecha, dcli_anufis, dcli_crerecibo, dcli_impreso, dcli_invmon,
            dcli_estatus, dcli_baseneta, dcli_cxc, dcli_dcto, dcli_otroimp,
            dcli_mtocomisio, dcli_mtoiva, dcli_neto, dcli_numpag, dcli_otros, dcli_plazo,
            dcli_recargo, dclli_valcamb, dcli_dctobs, dcli_totdivi, dcli_descitem,
            dcli_descdoc, dcli_subbase, doc_impo, dcli_cantproduc, dcli_aprob1,
            dcli_aprob2, dcli_aprob3, dcli_impresora, dcli_caja, dcli_cerrado,
            dcli_cosfac, dcli_cosfac_n, dcli_cosfac_i, dcli_base_n, dcli_base_i,
            dcli_saldo, dcli_facafe2, dcli_subtotal, dcli_ivaGN, dcli_ivaRD
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Aquí irían todos los valores correspondientes
        # Esta es una implementación básica que necesitaría ser completada
        return sql

    def acumularCostos(self, costoPromedio: Decimal, cantidad: int, procedencia: str) -> None:
        """Acumula costos según la procedencia."""
        costo_total = costoPromedio * cantidad
        if procedencia == "Nacional":
            self.costo_nacional += costo_total
        elif procedencia == "Importado":
            self.costo_importado += costo_total

    def restarCosto(self, costoPromedio: Decimal, cantidad: int, procedencia: str) -> None:
        """Resta costos según la procedencia."""
        costo_total = costoPromedio * cantidad
        if procedencia == "Nacional":
            self.costo_nacional -= costo_total
        elif procedencia == "Importado":
            self.costo_importado -= costo_total

    def acumularBases2(self, cantidad: int, precio: Decimal, procedencia: str) -> None:
        """Acumula bases según la procedencia."""
        total = precio * cantidad
        if procedencia == "Nacional":
            self.base_nacional += total
        elif procedencia == "Importado":
            self.base_importada += total

    def restarBases2(self, cantidad: int, precio: Decimal, procedencia: str) -> None:
        """Resta bases según la procedencia."""
        total = precio * cantidad
        if procedencia == "Nacional":
            self.base_nacional -= total
        elif procedencia == "Importado":
            self.base_importada -= total

    def guardarProntoPagos(self, fact: 'Factura') -> None:
        """Guarda la configuración de pronto pago."""
        # Implementar lógica para guardar pronto pagos
        pass