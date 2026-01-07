import mysql.connector
from mysql.connector import Error, pooling
import logging
from config import DATABASE_CONFIG

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConexionBD:
    def __init__(self, db_name='db1', timeout=None):
        self.db_name = db_name
        self.timeout = timeout
        self.connection_pool = None
        self._init_pool()

    def _init_pool(self):
        """Inicializa el pool de conexiones."""
        try:
            config = {
                'host': DATABASE_CONFIG['host'],
                'user': DATABASE_CONFIG['user'],
                'password': DATABASE_CONFIG['password'],
                'port': DATABASE_CONFIG['port'],
                'database': DATABASE_CONFIG['databases'].get(self.db_name, DATABASE_CONFIG['databases']['db1']),
                'pool_name': 'lebrun_pool',
                'pool_size': 5,  # Número de conexiones en el pool
                'connect_timeout': self.timeout or 10
            }
            self.connection_pool = pooling.MySQLConnectionPool(**config)
            logger.info(f"Pool de conexiones inicializado para la base de datos '{config['database']}'")
        except Error as e:
            logger.error(f"Error al inicializar el pool de conexiones: {e}")
            raise

    def get_connection(self):
        """Obtiene una conexión del pool."""
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logger.error(f"Error al obtener conexión del pool: {e}")
            raise

    def ejecutar_query_dr(self, query, timeout=None):
        """
        Ejecuta una consulta y devuelve un cursor (equivalente a DataReader).
        El cursor debe cerrarse manualmente.
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            if timeout:
                cursor.execute(query, timeout=timeout)
            else:
                cursor.execute(query)
            return cursor  # Devuelve el cursor para iterar resultados
        except Error as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            raise

    def ejecutar_query_ds(self, query):
        """
        Ejecuta una consulta y devuelve los resultados como lista de diccionarios (equivalente a DataSet).
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def sentencias_numero_filas(self, query):
        """
        Ejecuta una consulta de modificación (INSERT, UPDATE, DELETE) y devuelve el número de filas afectadas.
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            return cursor.rowcount
        except Error as e:
            logger.error(f"Error al ejecutar consulta: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def f_data_table(self, query, timeout=None):
        """
        Ejecuta una consulta y devuelve los resultados como lista de diccionarios (equivalente a DataTable).
        """
        return self.ejecutar_query_ds(query)  # Reutiliza el método anterior

    def modificar_conexion_string(self, db_num):
        """
        Cambia la base de datos (1: db1, 2: db2, 3: db3).
        """
        db_map = {1: 'db1', 2: 'db2', 3: 'db3'}
        if db_num in db_map:
            self.db_name = db_map[db_num]
            self._init_pool()  # Reinicia el pool con la nueva DB
        else:
            raise ValueError("Número de base de datos inválido")

    def close_all_connections(self):
        """Cierra todas las conexiones del pool (para limpieza)."""
        if self.connection_pool:
            self.connection_pool._remove_connections()

# Función de compatibilidad para el código existente
def connect_to_database(db_name):
    conn_bd = ConexionBD(db_name)
    return conn_bd

def close_connection(conn_bd):
    if isinstance(conn_bd, ConexionBD):
        conn_bd.close_all_connections()
    else:
        logger.warning("close_connection recibió un objeto no válido")