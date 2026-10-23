"""Reglas de multas. Funciones puras"""
from datetime import date

from nucleo.tipos import Parametros


def dias_retraso(fecha_prevista_devolucion: date, fecha_devolucion_real: date) -> int:
    """Días de retraso de una devolución; 0 si se devolvió a tiempo."""
    diferencia = (fecha_devolucion_real - fecha_prevista_devolucion).days
    return max(0, diferencia)


def calcular_multa(dias: int, parametros: Parametros) -> float:
    """Valor de la multa: días de retraso por el valor diario configurado."""
    if dias < 0:
        raise ValueError("Los días de retraso no pueden ser negativos")
    return dias * parametros.valor_multa_por_dia