"""Pruebas de las reglas de multas (RF19)."""
from datetime import date

import pytest

from nucleo.reglas_multa import calcular_multa, dias_retraso
from nucleo.tipos import Parametros


# ---------- dias_retraso ----------

def test_devolucion_a_tiempo_no_tiene_retraso():
    assert dias_retraso(date(2026, 10, 20), date(2026, 10, 18)) == 0


def test_devolucion_el_ultimo_dia_no_tiene_retraso():
    assert dias_retraso(date(2026, 10, 20), date(2026, 10, 20)) == 0


def test_devolucion_un_dia_tarde_tiene_un_dia_de_retraso():
    assert dias_retraso(date(2026, 10, 20), date(2026, 10, 21)) == 1


def test_devolucion_varios_dias_tarde():
    assert dias_retraso(date(2026, 10, 20), date(2026, 10, 27)) == 7


def test_retraso_cruzando_fin_de_mes():
    assert dias_retraso(date(2026, 10, 30), date(2026, 11, 2)) == 3


# ---------- calcular_multa ----------

def test_sin_retraso_la_multa_es_cero():
    assert calcular_multa(0, Parametros(15, 1000.0)) == 0.0


def test_multa_es_dias_por_valor_diario():
    assert calcular_multa(3, Parametros(15, 1000.0)) == 3000.0


def test_multa_usa_el_valor_configurado():
    assert calcular_multa(4, Parametros(15, 500.0)) == 2000.0


def test_dias_negativos_son_invalidos():
    with pytest.raises(ValueError):
        calcular_multa(-1, Parametros(15, 1000.0))