/**
 * Lebrun Facturación - JavaScript Personalizado
 * Funciones comunes y utilidades para la interfaz web
 */

// Configuración global
const CONFIG = {
  toastDuration: 5000,
  animationDuration: 300,
  debounceDelay: 300,
};

// Funciones de utilidad
const Utils = {
  /**
   * Muestra un toast de notificación
   * @param {string} message - Mensaje a mostrar
   * @param {string} type - Tipo de toast (success, error, warning, info)
   */
  showToast: function (message, type = "info") {
    const toastContainer =
      document.querySelector(".toast-container") || this.createToastContainer();

    const toastColors = {
      success: "#28a745",
      error: "#dc3545",
      warning: "#ffc107",
      info: "#17a2b8",
    };

    const toast = document.createElement("div");
    toast.className = "toast align-items-center text-white border-0 fade-in";
    toast.style.cssText = `
      background-color: ${toastColors[type] || toastColors.info};
      margin-bottom: 10px;
      min-width: 300px;
    `;
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">
          <i class="fas ${this.getIconForType(type)} me-2"></i>
          ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.remove()"></button>
      </div>
    `;

    toastContainer.appendChild(toast);

    // Auto-remover después de la duración
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, CONFIG.toastDuration);
  },

  /**
   * Crea el contenedor de toasts si no existe
   */
  createToastContainer: function () {
    const container = document.createElement("div");
    container.className = "toast-container position-fixed top-0 end-0 p-3";
    container.style.zIndex = "9999";
    document.body.appendChild(container);
    return container;
  },

  /**
   * Obtiene el icono apropiado para el tipo de toast
   */
  getIconForType: function (type) {
    const icons = {
      success: "fa-check-circle",
      error: "fa-exclamation-triangle",
      warning: "fa-exclamation-circle",
      info: "fa-info-circle",
    };
    return icons[type] || icons.info;
  },

  /**
   * Formatea números como moneda
   * @param {number} amount - Monto a formatear
   * @param {string} currency - Moneda (default: Bs)
   */
  formatCurrency: function (amount, currency = "Bs") {
    return new Intl.NumberFormat("es-VE", {
      style: "currency",
      currency: currency === "Bs" ? "VES" : "USD",
      minimumFractionDigits: 2,
    }).format(amount);
  },

  /**
   * Formatea fechas
   * @param {Date|string} date - Fecha a formatear
   * @param {string} format - Formato deseado
   */
  formatDate: function (date, format = "DD/MM/YYYY") {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();

    switch (format) {
      case "DD/MM/YYYY":
        return `${day}/${month}/${year}`;
      case "YYYY-MM-DD":
        return `${year}-${month}-${day}`;
      default:
        return d.toLocaleDateString("es-VE");
    }
  },

  /**
   * Función debounce para optimizar eventos
   * @param {Function} func - Función a ejecutar
   * @param {number} wait - Tiempo de espera en ms
   */
  debounce: function (func, wait = CONFIG.debounceDelay) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  /**
   * Valida un formulario
   * @param {HTMLFormElement} form - Formulario a validar
   */
  validateForm: function (form) {
    const inputs = form.querySelectorAll(
      "input[required], select[required], textarea[required]"
    );
    let isValid = true;

    inputs.forEach((input) => {
      if (!input.value.trim()) {
        this.showFieldError(input, "Este campo es obligatorio");
        isValid = false;
      } else {
        this.clearFieldError(input);
      }
    });

    return isValid;
  },

  /**
   * Muestra error en un campo
   * @param {HTMLElement} field - Campo con error
   * @param {string} message - Mensaje de error
   */
  showFieldError: function (field, message) {
    field.classList.add("is-invalid");
    let errorElement = field.parentElement.querySelector(".invalid-feedback");
    if (!errorElement) {
      errorElement = document.createElement("div");
      errorElement.className = "invalid-feedback";
      field.parentElement.appendChild(errorElement);
    }
    errorElement.textContent = message;
  },

  /**
   * Limpia error de un campo
   * @param {HTMLElement} field - Campo a limpiar
   */
  clearFieldError: function (field) {
    field.classList.remove("is-invalid");
    const errorElement = field.parentElement.querySelector(".invalid-feedback");
    if (errorElement) {
      errorElement.remove();
    }
  },

  /**
   * Carga contenido dinámicamente
   * @param {string} url - URL a cargar
   * @param {string} target - Selector del elemento destino
   */
  loadContent: function (url, target) {
    const targetElement = document.querySelector(target);
    if (!targetElement) return;

    // Mostrar loading
    targetElement.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
        <p class="mt-2 text-muted">Cargando contenido...</p>
      </div>
    `;

    fetch(url)
      .then((response) => response.text())
      .then((html) => {
        targetElement.innerHTML = html;
      })
      .catch((error) => {
        console.error("Error cargando contenido:", error);
        targetElement.innerHTML = `
          <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle me-2"></i>
            Error al cargar el contenido. Por favor, inténtelo de nuevo.
          </div>
        `;
      });
  },
};

// Funciones específicas de la aplicación
const App = {
  /**
   * Inicializa la aplicación
   */
  init: function () {
    this.initTooltips();
    this.initFormValidation();
    this.initDynamicMenus();
    this.initKeyboardShortcuts();
    this.initAutoSave();
  },

  /**
   * Inicializa tooltips de Bootstrap
   */
  initTooltips: function () {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  },

  /**
   * Inicializa validación de formularios
   */
  initFormValidation: function () {
    document.addEventListener("submit", function (e) {
      const form = e.target;
      if (!Utils.validateForm(form)) {
        e.preventDefault();
        Utils.showToast(
          "Por favor, complete todos los campos obligatorios.",
          "error"
        );
      }
    });
  },

  /**
   * Inicializa menús dinámicos
   */
  initDynamicMenus: function () {
    // Funcionalidad para submenús
    document.addEventListener("click", function (e) {
      if (e.target.closest(".dropdown-submenu")) {
        e.stopPropagation();
      }
    });
  },

  /**
   * Inicializa atajos de teclado
   */
  initKeyboardShortcuts: function () {
    document.addEventListener("keydown", function (e) {
      // Ctrl + S para guardar
      if (e.ctrlKey && e.key === "s") {
        e.preventDefault();
        const saveBtn = document.querySelector('[data-shortcut="save"]');
        if (saveBtn) saveBtn.click();
      }

      // Ctrl + N para nuevo
      if (e.ctrlKey && e.key === "n") {
        e.preventDefault();
        const newBtn = document.querySelector('[data-shortcut="new"]');
        if (newBtn) newBtn.click();
      }

      // Escape para cerrar modales
      if (e.key === "Escape") {
        const modals = document.querySelectorAll(".modal.show");
        modals.forEach((modal) => {
          const bsModal = bootstrap.Modal.getInstance(modal);
          if (bsModal) bsModal.hide();
        });
      }
    });
  },

  /**
   * Inicializa auto-guardado
   */
  initAutoSave: function () {
    const forms = document.querySelectorAll("[data-autosave]");
    forms.forEach((form) => {
      const inputs = form.querySelectorAll("input, textarea, select");
      inputs.forEach((input) => {
        input.addEventListener(
          "input",
          Utils.debounce(function () {
            // Implementar auto-guardado aquí
            console.log("Auto-guardando...", input.name);
          }, 2000)
        );
      });
    });
  },

  /**
   * Confirma una acción destructiva
   * @param {string} message - Mensaje de confirmación
   * @param {Function} callback - Función a ejecutar si confirma
   */
  confirmAction: function (message, callback) {
    if (confirm(message)) {
      callback();
    }
  },

  /**
   * Exporta datos a Excel
   * @param {Array} data - Datos a exportar
   * @param {string} filename - Nombre del archivo
   */
  exportToExcel: function (data, filename) {
    // Implementar exportación a Excel
    Utils.showToast("Función de exportación en desarrollo", "info");
  },

  /**
   * Imprime el contenido actual
   */
  printContent: function () {
    window.print();
  },
};

// Funciones específicas de módulos
const Facturacion = {
  /**
   * Calcula totales de factura
   */
  calcularTotales: function () {
    const filas = document.querySelectorAll(".factura-item");
    let subtotal = 0;

    filas.forEach((fila) => {
      const cantidad = parseFloat(fila.querySelector(".cantidad").value) || 0;
      const precio = parseFloat(fila.querySelector(".precio").value) || 0;
      const total = cantidad * precio;

      fila.querySelector(".total").value = total.toFixed(2);
      subtotal += total;
    });

    // Calcular IVA y total
    const iva = subtotal * 0.16; // 16% IVA
    const total = subtotal + iva;

    document.getElementById("subtotal").value = subtotal.toFixed(2);
    document.getElementById("iva").value = iva.toFixed(2);
    document.getElementById("total").value = total.toFixed(2);
  },

  /**
   * Agrega una nueva fila a la factura
   */
  agregarFila: function () {
    const tbody = document.querySelector("#factura-items tbody");
    const rowCount = tbody.children.length + 1;

    const newRow = document.createElement("tr");
    newRow.className = "factura-item";
    newRow.innerHTML = `
      <td><input type="text" class="form-control" name="codigo_${rowCount}" placeholder="Código"></td>
      <td><input type="text" class="form-control" name="descripcion_${rowCount}" placeholder="Descripción"></td>
      <td><input type="number" class="form-control cantidad" name="cantidad_${rowCount}" value="1" min="0" step="0.01"></td>
      <td><input type="number" class="form-control precio" name="precio_${rowCount}" value="0.00" min="0" step="0.01"></td>
      <td><input type="number" class="form-control total" name="total_${rowCount}" value="0.00" readonly></td>
      <td>
        <button type="button" class="btn btn-sm btn-danger" onclick="Facturacion.eliminarFila(this)">
          <i class="fas fa-trash"></i>
        </button>
      </td>
    `;

    tbody.appendChild(newRow);

    // Agregar event listeners
    newRow
      .querySelector(".cantidad")
      .addEventListener("input", this.calcularTotales);
    newRow
      .querySelector(".precio")
      .addEventListener("input", this.calcularTotales);
  },

  /**
   * Elimina una fila de la factura
   */
  eliminarFila: function (button) {
    button.closest("tr").remove();
    this.calcularTotales();
  },
};

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
  App.init();

  // Hacer funciones globales disponibles
  window.Utils = Utils;
  window.App = App;
  window.Facturacion = Facturacion;
  window.showToast = Utils.showToast;
});

// Exportar para uso en módulos
if (typeof module !== "undefined" && module.exports) {
  module.exports = { Utils, App, Facturacion };
}
