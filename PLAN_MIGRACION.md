# Plan de Migración: LebrunFacturacion de C# a Python

**Fecha de Creación:** 7 de enero de 2026  
**Proyecto Original:** LebrunFacturacion4 - compilot 4\lebrun\lebrun  
**Proyecto Destino:** LebrunFacturacion-Py

Este documento detalla el orden recomendado para migrar el proyecto de C# a Python, basado en la estructura del código original. La migración se divide en fases priorizadas para asegurar una transición eficiente, con mejoras en mantenibilidad, seguridad y modernidad.

## Objetivos Generales

- Migrar la funcionalidad core del sistema de facturación.
- Mejorar el código con mejores prácticas de Python (OOP, manejo de errores, logging, etc.).
- Usar librerías modernas para BD, UI y testing.
- Mantener compatibilidad con la configuración existente (bases de datos MySQL).

## Fases de Migración

### Fase 1: clasesData (Prioridad Alta - Base Fundamental)

**Duración Estimada:** 1-2 días  
**Razón:** Es la base del sistema; incluye conexión a BD y utilidades esenciales. Ya tienes `database.py` como base.

**Archivos a Migrar:**

- `ConexionBD.cs` → **Completado:** Mejorado `database.py` con clase `ConexionBD`, pools de conexiones, métodos equivalentes (ejecutar_query_dr, ejecutar_query_ds, etc.), y logging.
- `globales.cs` → **Completado:** Variables globales fusionadas en `config.py` como diccionario `GLOBALES`. Método `ConvertirListaADataTable` convertido a funciones en `utils.py`.
- `UsuarioSistema.cs` → **Completado:** Clase `Usuario` creada en `models.py` con métodos de autenticación y búsqueda.
- `Compania.cs` → **Completado:** Clase `Compania` expandida en `models.py` con propiedades y métodos para obtener compañías.
- `FuncionesTexbox.cs` → Módulo `utils.py` con validaciones de entrada.
- `Inputbox.cs` → Utilidades para diálogos de entrada (usar `tkinter`).

**Mejoras:**

- Usar `logging` para errores y depuración.
- Implementar excepciones personalizadas.
- Agregar `dotenv` para variables de entorno sensibles.
- Crear tests unitarios con `pytest`.

**Criterios de Finalización:**

- Conexión a BD funcional y probada.
- Utilidades básicas disponibles (validaciones, globales).

### Fase 2: clases (Prioridad Media - Lógica de Negocio)

**Duración Estimada:** 3-5 días  
**Razón:** Depende de la Fase 1; contiene la lógica core del negocio.

**Archivos a Migrar:**

- `bancos/` → Módulo `bancos.py` con clase `Banco` y métodos CRUD.
- `clientes/` → Módulo `clientes.py` con clase `Cliente`.
- `complementos/` → Módulo `complementos.py` para funcionalidades adicionales.
- `contabilidad/` → Módulo `contabilidad.py` para operaciones contables.
- `facturacion/` → Módulo `facturacion.py` con clase `Factura`.
- `vendedores/` → Módulo `vendedores.py` con clase `Vendedor`.

**Mejoras:**

- Refactorizar consultas SQL a usar SQLAlchemy (ORM) para mayor seguridad.
- Implementar async/await si hay operaciones pesadas.
- Agregar validaciones y manejo de errores.
- Crear tests unitarios para cada módulo.

**Criterios de Finalización:**

- Todas las clases migradas y funcionales.
- Consultas a BD probadas y optimizadas.

### Fase 3: formularios (Prioridad Baja - Interfaz de Usuario)

**Duración Estimada:** 5-7 días  
**Razón:** Depende de las fases anteriores; la UI se construye sobre la lógica.

**Archivos a Migrar:**

- `administracion/`, `bancos/`, `clientes/`, etc. → Módulos UI como `ui_administracion.py`, `ui_bancos.py`.
- Convertir formularios de Windows Forms a GUI en Python.

**Opciones de Framework:**

- **Tkinter** (simple, incluido en Python).
- **PyQt/PySide** (recomendado para interfaces complejas).

**Mejoras:**

- Diseñar UI moderna y responsiva.
- Separar lógica de UI (patrón MVC).
- Agregar estilos y temas.
- Crear tests de integración para UI.

**Criterios de Finalización:**

- Interfaz funcional y equivalente a la original.
- Navegación y eventos probados.

## Mejoras Generales Recomendadas

- **Estructura del Proyecto:** Organizar en paquetes (`models/`, `utils/`, `ui/`, `tests/`).
- **Versionado:** Usar Git para commits por fase/módulo.
- **Testing:** Implementar `pytest` desde la Fase 1.
- **Documentación:** Actualizar `README.md` con guías de uso.
- **Seguridad:** Evitar hardcodear credenciales; usar variables de entorno.
- **Performance:** Optimizar consultas y usar caching si es necesario.

## Notas Finales

- **Seguimiento:** Marca cada fase como "En Progreso", "Completada" o "Pendiente" en este documento.
- **Dependencias:** Actualizar `requirements.txt` con nuevas librerías (ej. `sqlalchemy`, `pyqt5`).
- **Riesgos:** Si encuentras dependencias complejas, prioriza funcionalidad core.
- **Contacto:** Si necesitas ayuda en una fase específica, consulta este plan.

**Estado Actual:** Fase 1 en progreso (ConexionBD.cs, globales.cs, UsuarioSistema.cs y Compania.cs completados).
