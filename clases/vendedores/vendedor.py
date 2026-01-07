"""
Módulo para la clase Vendedor.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from clasesData.database import ConexionBD
import logging

logger = logging.getLogger(__name__)

class Vendedor:
    """Clase para gestionar vendedores, basada en Vendedor.cs."""

    def __init__(self, timeout=None):
        self.db = ConexionBD('db1')  # sisadm
        self.nombre = None
        self.cedula = None
        self.cargo = None
        self.status = None
        self.codigo_v = None

    # Propiedades
    @property
    def Nombre(self):
        return self.nombre

    @Nombre.setter
    def Nombre(self, value):
        self.nombre = value

    @property
    def Cedula(self):
        return self.cedula

    @Cedula.setter
    def Cedula(self, value):
        self.cedula = value

    @property
    def Cargo(self):
        return self.cargo

    @Cargo.setter
    def Cargo(self, value):
        self.cargo = value

    @property
    def Status(self):
        return self.status

    @Status.setter
    def Status(self, value):
        self.status = value

    @property
    def CodigoV(self):
        return self.codigo_v

    @CodigoV.setter
    def CodigoV(self, value):
        self.codigo_v = value

    def data_lbx_vendedores(self):
        """Obtiene lista de vendedores para listbox."""
        query = "SELECT ven_codigo, ven_nombre, ven_cedula, ven_cargo, ven_status FROM admvendedor WHERE ven_lbxven = TRUE LIMIT 35;"
        try:
            return self.db.ejecutar_query_ds(query)
        except Exception as e:
            logger.error(f"Error obteniendo lista de vendedores: {e}")
            return []

    def vendedor_buscado(self, vendedor_buscar):
        """Busca vendedores por código o nombre."""
        query = """
        SELECT ven_codigo, ven_nombre, ven_cedula, ven_cargo, ven_status
        FROM admvendedor WHERE ven_codigo LIKE %s OR ven_nombre LIKE %s;
        """
        try:
            return self.db.ejecutar_query_ds(query, (f"%{vendedor_buscar}%", f"%{vendedor_buscar}%"))
        except Exception as e:
            logger.error(f"Error buscando vendedor: {e}")
            return []

    def get_nombre_ven(self, id_vendedor):
        """Obtiene el nombre del vendedor por ID."""
        query = "SELECT ven_nombre FROM admvendedor WHERE ven_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (id_vendedor,))
            if results:
                return results[0]['ven_nombre']
            return None
        except Exception as e:
            logger.error(f"Error obteniendo nombre del vendedor {id_vendedor}: {e}")
            return None

    def cargar_datos_vendedor(self):
        """Carga datos del vendedor actual."""
        query = "SELECT ven_codigo, ven_nombre, ven_status FROM admvendedor WHERE ven_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (self.codigo_v,))
            if results:
                row = results[0]
                self.codigo_v = row['ven_codigo']
                self.nombre = row['ven_nombre']
                self.status = row['ven_status']
        except Exception as e:
            logger.error(f"Error cargando datos del vendedor {self.codigo_v}: {e}")

    def existe_vendedor(self, codigo_vendedor):
        """Verifica si existe un vendedor."""
        query = "SELECT ven_nombre FROM admvendedor WHERE ven_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (codigo_vendedor,))
            return len(results) > 0 and results[0]['ven_nombre'] != ""
        except Exception as e:
            logger.error(f"Error verificando existencia del vendedor {codigo_vendedor}: {e}")
            return False

    def esta_activo(self, codigo_vendedor):
        """Verifica si el vendedor está activo."""
        query = "SELECT ven_status FROM admvendedor WHERE ven_codigo = %s;"
        try:
            results = self.db.ejecutar_query_ds(query, (codigo_vendedor,))
            return len(results) > 0 and results[0]['ven_status'] == "Activo"
        except Exception as e:
            logger.error(f"Error verificando estado del vendedor {codigo_vendedor}: {e}")
            return False

    def nombre_vende(self, id_vendedor):
        """Alias para get_nombre_ven."""
        return self.get_nombre_ven(id_vendedor)