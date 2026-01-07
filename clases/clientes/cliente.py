"""
Módulo para la clase Cliente.
"""

import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from clasesData.database import ConexionBD
import logging

logger = logging.getLogger(__name__)

class Cliente:
    """Clase para gestionar clientes, basada en Clientes.cs."""

    def __init__(self, timeout=None):
        self.db = ConexionBD('db1', timeout)  # Usar db1 (sisadm) para clientes
        self.codigo = None
        self.nombre = None
        self.rif = None
        self.nif = None
        self.categoria = None
        self.direccion = None
        self.direccion2 = None
        self.direccion_envio = None
        self.representante = None
        self.zona_geografica = None
        self.zona_postal = None
        self.telefono = None
        self.fax = None
        self.email = None
        self.tipo_negocio = None
        self.transporte = None
        self.vendedor = None
        self.comision_ven = None
        self.cobrador = None
        self.comision_cobrador = None
        self.dia_cobro = None
        self.tipo_lista = None
        self.situacion = None
        self.fecha_inicio_vaca = None
        self.fecha_fin_vaca = None
        self.tipo_persona = None
        self.cliente_plan_c = None
        self.cliente_auxiliar = None
        self.observaciones = None
        self.condicion_pago = None
        self.divisa_cliente = None
        self.descuento_enventas = None
        self.codigo_condicion_pago = None
        self.cuenta_manor = None
        self.auxiliar_c = None
        self.contribuyente = None
        self.id_tipo_negocio = None
        self.descuento2 = None
        self.descuento3 = None
        self.limite_credito = None
        self.fecha_registro = None
        self.fecha_ultima_compra = None

    # Propiedades (solo algunas principales, agregar más si es necesario)
    @property
    def Codigo(self):
        return self.codigo

    @Codigo.setter
    def Codigo(self, value):
        self.codigo = value

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
    def Direccion(self):
        return self.direccion

    @Direccion.setter
    def Direccion(self, value):
        self.direccion = value

    @property
    def Telefono(self):
        return self.telefono

    @Telefono.setter
    def Telefono(self, value):
        self.telefono = value

    @property
    def Email(self):
        return self.email

    @Email.setter
    def Email(self, value):
        self.email = value

    # Más propiedades pueden agregarse según necesidad

    def lbx_clientes(self):
        """Obtiene lista de clientes para listbox."""
        query = "SELECT cli_codigo, cli_nombre, cli_rif, cli_categoria, cli_situacion FROM admclientes LIMIT 45;"
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo lista de clientes: {e}")
            return []

    def cliente_buscado(self, cliente_buscar):
        """Busca clientes por código, nombre o RIF."""
        query = """
        SELECT cli_codigo, cli_nombre, cli_rif, cli_categoria, cli_situacion
        FROM admclientes WHERE cli_codigo LIKE %s OR cli_nombre LIKE %s OR cli_rif LIKE %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (f"%{cliente_buscar}%", f"%{cliente_buscar}%", f"%{cliente_buscar}%"))
        except Exception as e:
            logger.error(f"Error buscando cliente: {e}")
            return []

    def ingresar_cliente(self):
        """Registra un nuevo cliente."""
        # Query simplificada basada en el original (ajustar campos según necesidad)
        query = """
        INSERT INTO admclientes (cli_codigo, cli_nombre, cli_rif, cli_vendedor, cli_telefono, cli_direc1,
        cli_fechareg, cli_tipoper, cli_contribuyen, cli_categoria, cli_situacion, cli_condipag, cli_divisa,
        cli_descuento, cli_credito, cli_inivaca, cli_finvaca)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        fecha_sistema = datetime.now().strftime('%Y-%m-%d')
        try:
            self.db.sentencias_numero_filas(query, (
                self.codigo, self.nombre, self.rif, self.vendedor, self.telefono, self.direccion,
                fecha_sistema, self.tipo_persona, self.contribuyente, self.categoria, self.situacion,
                self.condicion_pago, self.divisa_cliente, self.descuento_enventas, self.limite_credito,
                self.fecha_inicio_vaca, self.fecha_fin_vaca
            ))
            logger.info(f"Cliente {self.codigo} registrado exitosamente.")
            return True
        except Exception as e:
            logger.error(f"Error registrando cliente: {e}")
            return False

    def existe_cliente(self):
        """Verifica si el cliente existe."""
        query = "SELECT COUNT(*) as count FROM admclientes WHERE cli_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (self.codigo,))
            return results[0]['count'] > 0 if results else False
        except Exception as e:
            logger.error(f"Error verificando existencia del cliente: {e}")
            return False

    def precio_cliente(self):
        """Obtiene precios del cliente."""
        query = "SELECT * FROM admprecioscliente WHERE pre_cli_codigo = %s;"
        try:
            return self.db.ejecutar_query_ds(query, (self.codigo,))
        except Exception as e:
            logger.error(f"Error obteniendo precios del cliente: {e}")
            return []

    def cargar_datos_cliente(self):
        """Carga datos completos del cliente."""
        query = """
        SELECT * FROM admclientes WHERE cli_codigo = %s;
        """
        try:
            results = self.db.ejecutar_query_ds(query, (self.codigo,))
            if results:
                row = results[0]
                self.nombre = row.get('cli_nombre')
                self.rif = row.get('cli_rif')
                self.direccion = row.get('cli_direc1')
                # Cargar más campos según necesidad
            return results
        except Exception as e:
            logger.error(f"Error cargando datos del cliente: {e}")
            return []

    def condig_pag(self):
        """Obtiene condición de pago del cliente."""
        query = "SELECT cli_condipag FROM admclientes WHERE cli_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (self.codigo,))
            return results[0]['cli_condipag'] if results else None
        except Exception as e:
            logger.error(f"Error obteniendo condición de pago: {e}")
            return None

    def modificar_cliente(self):
        """Modifica datos del cliente."""
        query = """
        UPDATE admclientes SET cli_nombre=%s, cli_rif=%s, cli_vendedor=%s, cli_telefono=%s,
        cli_direc1=%s, cli_tipoper=%s, cli_contribuyen=%s, cli_categoria=%s, cli_situacion=%s,
        cli_condipag=%s, cli_divisa=%s, cli_descuento=%s, cli_credito=%s, cli_inivaca=%s,
        cli_finvaca=%s WHERE cli_codigo=%s;
        """
        try:
            self.db.sentencias_numero_filas(query, (
                self.nombre, self.rif, self.vendedor, self.telefono, self.direccion,
                self.tipo_persona, self.contribuyente, self.categoria, self.situacion,
                self.condicion_pago, self.divisa_cliente, self.descuento_enventas,
                self.limite_credito, self.fecha_inicio_vaca, self.fecha_fin_vaca, self.codigo
            ))
            logger.info(f"Cliente {self.codigo} modificado exitosamente.")
            return True
        except Exception as e:
            logger.error(f"Error modificando cliente: {e}")
            return False

    def esta_activo(self, cod_cli):
        """Verifica si el cliente está activo."""
        query = "SELECT cli_situacion FROM admclientes WHERE cli_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (cod_cli,))
            return results[0]['cli_situacion'] == 'A' if results else False
        except Exception as e:
            logger.error(f"Error verificando estado del cliente: {e}")
            return False

    def buscar_cliente_unico(self, codigo):
        """Busca un cliente específico."""
        query = "SELECT * FROM admclientes WHERE cli_codigo = %s;"
        try:
            return self.db.ejecutar_query_ds(query, (codigo,))
        except Exception as e:
            logger.error(f"Error buscando cliente único: {e}")
            return []

    def suspender_clientes(self, cliente):
        """Suspende un cliente."""
        query = "UPDATE admclientes SET cli_situacion = 'S' WHERE cli_codigo = %s;"
        try:
            self.db.sentencias_numero_filas(query, (cliente,))
            logger.info(f"Cliente {cliente} suspendido.")
        except Exception as e:
            logger.error(f"Error suspendiendo cliente: {e}")
            raise

    def habilitar_cliente(self, cliente):
        """Habilita un cliente."""
        query = "UPDATE admclientes SET cli_situacion = 'A' WHERE cli_codigo = %s;"
        try:
            self.db.sentencias_numero_filas(query, (cliente,))
            logger.info(f"Cliente {cliente} habilitado.")
        except Exception as e:
            logger.error(f"Error habilitando cliente: {e}")
            raise

    def actualizar_cuenta_ma(self, m, a):
        """Actualiza cuenta manor y auxiliar."""
        query = "UPDATE admclientes SET cli_cuentamanor = %s, cli_auxiliar = %s WHERE cli_codigo = %s;"
        try:
            self.db.sentencias_numero_filas(query, (m, a, self.codigo))
            logger.info(f"Cuenta MA actualizada para cliente {self.codigo}.")
        except Exception as e:
            logger.error(f"Error actualizando cuenta MA: {e}")
            raise

    def limpiar_cliente(self):
        """Limpia los datos del cliente."""
        self.codigo = None
        self.nombre = None
        self.rif = None
        # Limpiar más campos según necesidad

    def documentos_vencidos(self):
        """Verifica si el cliente tiene documentos vencidos."""
        # Implementar lógica de verificación de documentos vencidos
        # Por simplicidad, retornar False
        return False

    def saldo_actual_salcli(self, codigo_cliente, status):
        """Obtiene saldo actual del cliente."""
        query = """
        SELECT SUM(sal_saldo) as saldo FROM admsaldoscli
        WHERE sal_codigo = %s AND sal_status = %s;
        """
        try:
            results = self.db.ejecutar_query_ds(query, (codigo_cliente, status))
            return results[0]['saldo'] if results and results[0]['saldo'] else 0
        except Exception as e:
            logger.error(f"Error obteniendo saldo actual: {e}")
            return 0

    def saldo_vencido_salcli(self, codigo_cliente, status, fecha):
        """Obtiene saldo vencido del cliente."""
        query = """
        SELECT SUM(sal_saldo) as saldo FROM admsaldoscli
        WHERE sal_codigo = %s AND sal_status = %s AND sal_fecven < %s;
        """
        try:
            results = self.db.ejecutar_query_ds(query, (codigo_cliente, status, fecha))
            return results[0]['saldo'] if results and results[0]['saldo'] else 0
        except Exception as e:
            logger.error(f"Error obteniendo saldo vencido: {e}")
            return 0