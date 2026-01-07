LebrunFacturacion-Web/
├── app.py # Aplicación principal Flask
├── config.py # Configuración
├── requirements.txt # Dependencias
├── run.py # Script de ejecución
├── instance/ # Configuración de instancia
├── app/
│ ├── **init**.py
│ ├── models.py # Modelos de datos
│ ├── auth.py # Lógica de autenticación
│ ├── menu.py # Sistema de menús dinámicos
│ ├── routes/ # Rutas organizadas por módulo
│ │ ├── **init**.py
│ │ ├── auth.py # Rutas de autenticación
│ │ ├── dashboard.py # Dashboard principal
│ │ ├── facturacion.py
│ │ ├── clientes.py
│ │ ├── bancos.py
│ │ ├── complementos.py
│ │ ├── contabilidad.py
│ │ └── vendedores.py
│ ├── static/ # Archivos estáticos
│ │ ├── css/
│ │ │ ├── style.css
│ │ │ ├── bootstrap.min.css
│ │ │ └── material-design.css
│ │ ├── js/
│ │ │ ├── app.js
│ │ │ ├── bootstrap.bundle.min.js
│ │ │ └── jquery.min.js
│ │ ├── img/
│ │ └── fonts/
│ └── templates/ # Plantillas HTML
│ ├── base.html
│ ├── login.html
│ ├── dashboard.html
│ ├── facturacion/
│ │ ├── index.html
│ │ ├── factura_venta.html
│ │ └── nota_credito.html
│ ├── clientes/
│ │ ├── index.html
│ │ └── cliente_form.html
│ └── shared/
│ ├── navbar.html
│ ├── sidebar.html
│ └── modals.html
├── migrations/ # Migraciones de BD (si es necesario)
└── tests/ # Tests
└── **init**.py
