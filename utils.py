"""
Utilidades generales para el proyecto LebrunFacturacion-Py.
"""

import pandas as pd
from typing import List, Any, Dict

def convertir_lista_a_dataframe(lista: List[Any]) -> pd.DataFrame:
    """
    Convierte una lista de objetos a un DataFrame de pandas (equivalente a DataTable en C#).
    :param lista: Lista de objetos con atributos.
    :return: DataFrame con los datos.
    """
    if not lista:
        return pd.DataFrame()

    # Convertir objetos a diccionarios
    data = [vars(obj) for obj in lista]
    return pd.DataFrame(data)

def convertir_lista_a_lista_dict(lista: List[Any]) -> List[Dict[str, Any]]:
    """
    Convierte una lista de objetos a una lista de diccionarios.
    :param lista: Lista de objetos.
    :return: Lista de diccionarios.
    """
    if not lista:
        return []
    return [vars(obj) for obj in lista]

# Funciones de validación para campos de texto (basado en FuncionesTexbox.cs)
def validar_solo_decimales(texto: str) -> bool:
    """Valida si el texto permite solo decimales (equivalente a txtOnlyDecimal)."""
    if '.' in texto:
        return texto.replace('.', '').replace('\b', '').replace('\r', '').isdigit()
    else:
        return texto.replace('.', '').replace('\b', '').replace('\r', '').isdigit()

def validar_solo_numeros(texto: str) -> bool:
    """Valida si el texto contiene solo números (equivalente a OnlyNumbers)."""
    return texto.replace('\b', '').replace('\r', '').isdigit()

def validar_tab(texto: str) -> bool:
    """Permite tabulación en enter (equivalente a tab)."""
    return '\r' in texto  # En UI, manejar el evento

def validar_solo_numeros_con_tab(texto: str) -> bool:
    """Valida números con tabulación."""
    return validar_solo_numeros(texto) or '\r' in texto

# Diálogos de entrada (basado en Inputbox.cs)
def input_box(prompt: str, title: str = "Entrada") -> str:
    """
    Diálogo simple de entrada usando input() de consola.
    En una UI gráfica, reemplazar con tkinter.
    """
    print(f"{title}: {prompt}")
    return input("> ")