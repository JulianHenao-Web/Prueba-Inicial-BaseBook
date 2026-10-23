"""Pruebas de las reglas de préstamo (RF11, RF12, RF13)."""
from dataclasses import replace
from datetime import date

import pytest

from nucleo.reglas_prestamo import (
    cerrar_prestamo,
    crear_solicitud,
    puede_solicitar_prestamo,
    registrar_prestamo,
)
from nucleo.tipos import (
    ESTADO_CUENTA_INACTIVA,
    LIBRO_DISPONIBLE,
    LIBRO_PRESTADO,
    PRESTAMO_ACTIVO,
    PRESTAMO_DEVUELTO,
    PRESTAMO_SOLICITADO,
    PRESTAMO_VENCIDO,
    ROL_BIBLIOTECARIO,
    ROL_LECTOR,
    Libro,
    Parametros,
    Prestamo,
    Usuario,
)


def un_lector(**cambios):
    base = Usuario(1, "Ana Pérez", "100", "ana@correo.com", "300", "hash", ROL_LECTOR)
    return replace(base, **cambios)


def un_libro(**cambios):
    base = Libro(10, "978-1", "Cien años de soledad", "García Márquez",
                 "Novela", "Sudamericana", 1967)
    return replace(base, **cambios)


def una_solicitud():
    return crear_solicitud(5, un_lector(), un_libro(), date(2026, 10, 1))


PARAMETROS = Parametros(periodo_prestamo_dias=15, valor_multa_por_dia=1000.0)


# ---------- puede_solicitar_prestamo ----------

def test_lector_activo_y_libro_disponible_puede_solicitar():
    assert puede_solicitar_prestamo(un_lector(), un_libro()) is True


def test_libro_prestado_no_se_puede_solicitar():
    assert puede_solicitar_prestamo(un_lector(), un_libro(estado=LIBRO_PRESTADO)) is False


def test_cuenta_inactiva_no_puede_solicitar():
    lector = un_lector(estado_cuenta=ESTADO_CUENTA_INACTIVA)
    assert puede_solicitar_prestamo(lector, un_libro()) is False


def test_solo_un_lector_puede_solicitar():
    bibliotecario = un_lector(rol=ROL_BIBLIOTECARIO)
    assert puede_solicitar_prestamo(bibliotecario, un_libro()) is False


# ---------- crear_solicitud ----------

def test_solicitud_nace_en_estado_solicitado():
    p = una_solicitud()
    assert p.estado == PRESTAMO_SOLICITADO
    assert (p.id_prestamo, p.id_lector, p.id_libro) == (5, 1, 10)
    assert p.fecha_solicitud == date(2026, 10, 1)
    assert p.id_bibliotecario is None and p.fecha_prestamo is None


def test_solicitud_de_libro_no_disponible_lanza_error():
    with pytest.raises(ValueError):
        crear_solicitud(5, un_lector(), un_libro(estado=LIBRO_PRESTADO), date(2026, 10, 1))


# ---------- registrar_prestamo ----------

def test_registrar_prestamo_lo_deja_activo_con_fechas():
    p = registrar_prestamo(una_solicitud(), 7, date(2026, 10, 2), PARAMETROS)
    assert p.estado == PRESTAMO_ACTIVO
    assert p.id_bibliotecario == 7
    assert p.fecha_prestamo == date(2026, 10, 2)
    assert p.fecha_prevista_devolucion == date(2026, 10, 17)


def test_registrar_prestamo_respeta_el_periodo_configurado():
    p = registrar_prestamo(una_solicitud(), 7, date(2026, 10, 2), Parametros(7, 1000.0))
    assert p.fecha_prevista_devolucion == date(2026, 10, 9)


def test_registrar_prestamo_no_modifica_la_solicitud_original():
    solicitud = una_solicitud()
    registrar_prestamo(solicitud, 7, date(2026, 10, 2), PARAMETROS)
    assert solicitud.estado == PRESTAMO_SOLICITADO


def test_solo_se_registra_una_solicitud():
    activo = registrar_prestamo(una_solicitud(), 7, date(2026, 10, 2), PARAMETROS)
    with pytest.raises(ValueError):
        registrar_prestamo(activo, 7, date(2026, 10, 3), PARAMETROS)


# ---------- cerrar_prestamo ----------

def test_cerrar_prestamo_lo_deja_devuelto_con_fecha():
    activo = registrar_prestamo(una_solicitud(), 7, date(2026, 10, 2), PARAMETROS)
    cerrado = cerrar_prestamo(activo, date(2026, 10, 10))
    assert cerrado.estado == PRESTAMO_DEVUELTO
    assert cerrado.fecha_devolucion_real == date(2026, 10, 10)


def test_cerrar_prestamo_vencido_es_valido():
    activo = registrar_prestamo(una_solicitud(), 7, date(2026, 10, 2), PARAMETROS)
    vencido = replace(activo, estado=PRESTAMO_VENCIDO)
    assert cerrar_prestamo(vencido, date(2026, 10, 25)).estado == PRESTAMO_DEVUELTO


def test_no_se_puede_cerrar_una_solicitud():
    with pytest.raises(ValueError):
        cerrar_prestamo(una_solicitud(), date(2026, 10, 10))


def test_no_se_puede_cerrar_dos_veces():
    activo = registrar_prestamo(una_solicitud(), 7, date(2026, 10, 2), PARAMETROS)
    cerrado = cerrar_prestamo(activo, date(2026, 10, 10))
    with pytest.raises(ValueError):
        cerrar_prestamo(cerrado, date(2026, 10, 11))