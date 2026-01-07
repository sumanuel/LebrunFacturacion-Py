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
def validar_numero(texto: str) -> bool:
    """Valida si el texto es un número."""
    try:
        float(texto)
        return True
    except ValueError:
        return False

def validar_entero(texto: str) -> bool:
    """Valida si el texto es un entero."""
    try:
        int(texto)
        return True
    except ValueError:
        return False

def validar_email(texto: str) -> bool:
    """Valida si el texto es un email básico."""
    return '@' in texto and '.' in texto

# Diálogos de entrada (basado en Inputbox.cs)
def input_box(prompt: str, title: str = "Entrada") -> str:
    """
    Diálogo simple de entrada usando input() de consola.
    En una UI gráfica, reemplazar con tkinter.
    """
    print(f"{title}: {prompt}")
    return input("> ")