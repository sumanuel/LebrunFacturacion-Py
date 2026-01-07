import mysql.connector
from mysql.connector import Error
from config import DATABASE_CONFIG

def connect_to_database(db_name):
    """
    Conecta a una base de datos MySQL específica.
    :param db_name: Nombre de la base de datos (ej: 'db1', 'db2', 'db3')
    :return: Objeto de conexión o None si falla
    """
    try:
        config = {
            'host': DATABASE_CONFIG['host'],
            'user': DATABASE_CONFIG['user'],
            'password': DATABASE_CONFIG['password'],
            'port': DATABASE_CONFIG['port'],
            'database': DATABASE_CONFIG['databases'].get(db_name)
        }
        if not config['database']:
            raise ValueError(f"Base de datos '{db_name}' no encontrada en la configuración.")

        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print(f"Conexión exitosa a la base de datos '{config['database']}'")
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(connection):
    """
    Cierra la conexión a la base de datos.
    :param connection: Objeto de conexión
    """
    if connection and connection.is_connected():
        connection.close()
        print("Conexión cerrada.")

# Ejemplo de uso
if __name__ == "__main__":
    # Conectar a db1 (sisadm)
    conn = connect_to_database('db1')
    if conn:
        # Aquí puedes ejecutar consultas
        # Ejemplo: cursor = conn.cursor()
        # cursor.execute("SELECT * FROM alguna_tabla")
        close_connection(conn)