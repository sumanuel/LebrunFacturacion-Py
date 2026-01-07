from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)

@dataclass
class Factura:
    """
    Clase que representa una factura en el sistema de facturación.
    Equivalente a la clase Factura.cs del proyecto original.
    """

    # Atributos principales
    base_gn: Decimal = Decimal('0')
    base_ex: Decimal = Decimal('0')
    base_rd: Decimal = Decimal('0')
    iva_gn: Decimal = Decimal('0')
    iva_rd: Decimal = Decimal('0')
    iva_total: Decimal = Decimal('0')
    total_neto: Decimal = Decimal('0')
    total_base: Decimal = Decimal('0')
    descuento_items: Decimal = Decimal('0')
    costo_nacional: Decimal = Decimal('0')
    costo_importado: Decimal = Decimal('0')
    base_nacional: Decimal = Decimal('0')
    base_importada: Decimal = Decimal('0')

    # Strings
    factura_afectada: str = ""
    numero_fiscal_afectado: str = ""
    hora_afectada: str = ""
    fecha_afectada: str = ""
    eoc_afectado: str = ""
    correlativo_interno: str = ""
    tipo_documento: str = ""
    condicion: str = ""
    divisa: str = ""
    numero_fiscal: str = ""
    modelo_impresora: str = ""
    serie_impresora: str = ""
    dcli_aprob1: str = ""
    dcli_aprob2: str = ""
    dcli_aprob3: str = ""
    dcli_estado: str = ""
    dcli_expexp: str = ""
    ctd_codcta: str = ""
    numero_pedido: str = ""
    direccion_envio: str = ""
    dir_obra: str = ""
    certificado: str = ""
    nombre_reporte: str = ""
    peso: str = ""
    bultos: str = ""
    estatus: str = ""
    dias_pp1: str = ""
    dias_pp2: str = ""
    porcentaje_pp1: str = ""
    porcentaje_pp2: str = ""
    codigo_rechazo: str = ""
    dcli_anufis: str = ""

    # Fechas
    fecha_factura: datetime = datetime.now()

    # Números
    descuento_general: Decimal = Decimal('0')
    plazo_dias: int = 0
    total_items: int = 0
    maxima_cantidad_detalles: int = 0

    # Objetos relacionados
    cliente_facturar: Optional[Any] = None  # Clientes
    vendedor_factura: Optional[Any] = None  # Vendedor
    dgv_items: Optional[Any] = None  # DataGridView equivalente, quizás un DataFrame o lista

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