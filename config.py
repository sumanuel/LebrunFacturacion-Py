# Configuración de la base de datos basada en App.config
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'port': 3306,
    'databases': {
        'db1': 'sisadm',
        'db2': 'sysconf',
        'db3': 'sysconta'
    }
}

# Otras configuraciones relevantes
APP_SETTINGS = {
    'logs': 1,
    'portPrinter': 'COM1',
    'impresoraRecibo': 'POS-80',
    'imprimir': 1,
    'puerto': 'COM8',
    'mostrarCodigoArticulo': True,
    'mostrarSpooler': False,
    'es2k12': True,
    'flag21': 30,
    # Códigos de formas de pago fiscal
    'efectivobs': '03',
    'efectivodol': '02',
    'tarjeta': '09',
    'credito': '13',
    'cheque': '02',
    'transferencia': '01',
    'otros': '05',
    'divisaigtf': '20',
    'cambio': '02',
    'cashea': '07',
    'pagomovil': '06',
    # IGTF
    'igtf': 3,
    'activarigtf': True,
    # Pie de factura fiscal
    'pieFactura1': 'GRACIAS POR SU COMPRA',
    'pieFactura2': '',
    'pieFactura3': '',
    'pieFactura4': '',
    # Formato de impresión fiscal
    'maxcantdec': 3,
    'maxpreciodec': 2,
    'maxmonedadec': 2,
    # Configuración de relleno y factores
    'RellenoPrecio': 0,
    'RellenoCantidad': 0,
    'factorPrecio': 1,
    'factorCantidad': 1,
    'longitudPrecio': 2,
    'longitudCantidad': 3,
    # Intervalo de spooler
    'intervalo': 5
}