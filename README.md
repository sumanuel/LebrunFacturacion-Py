# LebrunFacturacion-Py

Migración del proyecto LebrunFacturacion de C# a Python.

## Configuración

1. Instalar dependencias:

   ```
   pip install -r requirements.txt
   ```

2. Asegurarse de que MySQL esté corriendo en localhost:3306 con las bases de datos configuradas.

## Archivos

- `config.py`: Configuraciones extraídas de App.config
- `database.py`: Funciones para conectar a la base de datos MySQL
- `requirements.txt`: Dependencias de Python

## Uso

Para conectar a una base de datos:

```python
from database import connect_to_database, close_connection

conn = connect_to_database('db1')  # Conecta a sisadm
if conn:
    # Ejecutar consultas aquí
    close_connection(conn)
```
