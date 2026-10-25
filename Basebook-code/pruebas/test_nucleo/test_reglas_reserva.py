"""Pruebas de las reglas de reserva (RF15)."""
from dataclasses import replace
from datetime import date

import pytest

from nucleo.reglas_reserva import (
    atender_reserva,
    cancelar_reserva,
    crear_reserva,
    puede_reservar,
    siguiente_en_cola,
)
from nucleo.tipos import (
    ESTADO_CUENTA_INACTIVA,
    LIBRO_DISPONIBLE,
    LIBRO_PRESTADO,
    LIBRO_RESERVADO,
    RESERVA_ATENDIDA,
    RESERVA_CANCELADA,
    RESERVA_PENDIENTE,
    ROL_BIBLIOTECARIO,
    ROL_LECTOR,
    Libro,
    Reserva,
    Usuario,
)


def un_lector(**cambios):
    base = Usuario(1, "Ana Pérez", "100", "ana@correo.com", "300", "hash", ROL_LECTOR)
    return replace(base, **cambios)


def un_libro(**cambios):
    base = Libro(10, "978-1", "Cien años de soledad", "García Márquez",
                 "Novela", "Sudamericana", 1967, estado=LIBRO_PRESTADO)
    return replace(base, **cambios)


def una_reserva(id_reserva=1, id_lector=1, id_libro=10, dia=1, estado=RESERVA_PENDIENTE):
    return Reserva(id_reserva, id_lector, id_libro, date(2026, 10, dia), estado=estado)


# ---------- puede_reservar ----------

def test_puede_reservar_un_libro_prestado():
    assert puede_reservar(un_lector(), un_libro(), []) is True


def test_puede_reservar_un_libro_reservado_por_otro():
    assert puede_reservar(un_lector(), un_libro(estado=LIBRO_RESERVADO), []) is True


def test_no_se_reserva_un_libro_disponible():
    assert puede_reservar(un_lector(), un_libro(estado=LIBRO_DISPONIBLE), []) is False


def test_cuenta_inactiva_no_puede_reservar():
    lector = un_lector(estado_cuenta=ESTADO_CUENTA_INACTIVA)
    assert puede_reservar(lector, un_libro(), []) is False


def test_solo_un_lector_puede_reservar():
    assert puede_reservar(un_lector(rol=ROL_BIBLIOTECARIO), un_libro(), []) is False


def test_no_puede_reservar_dos_veces_el_mismo_libro():
    assert puede_reservar(un_lector(), un_libro(), [una_reserva()]) is False


def test_reserva_atendida_anterior_no_impide_reservar_de_nuevo():
    previa = una_reserva(estado=RESERVA_ATENDIDA)
    assert puede_reservar(un_lector(), un_libro(), [previa]) is True


def test_reserva_pendiente_de_otro_lector_no_impide_reservar():
    otra = una_reserva(id_lector=99)
    assert puede_reservar(un_lector(), un_libro(), [otra]) is True


def test_reserva_pendiente_de_otro_libro_no_impide_reservar():
    otra = una_reserva(id_libro=77)
    assert puede_reservar(un_lector(), un_libro(), [otra]) is True


# ---------- crear_reserva ----------

def test_crear_reserva_nace_pendiente():
    r = crear_reserva(3, un_lector(), un_libro(), [], date(2026, 10, 5))
    assert r.estado == RESERVA_PENDIENTE
    assert (r.id_reserva, r.id_lector, r.id_libro) == (3, 1, 10)
    assert r.fecha_reserva == date(2026, 10, 5)


def test_crear_reserva_invalida_lanza_error():
    with pytest.raises(ValueError):
        crear_reserva(3, un_lector(), un_libro(estado=LIBRO_DISPONIBLE), [], date(2026, 10, 5))


# ---------- siguiente_en_cola ----------

def test_cola_vacia_no_tiene_siguiente():
    assert siguiente_en_cola([]) is None


def test_siguiente_es_la_reserva_pendiente_mas_antigua():
    cola = [una_reserva(1, dia=9), una_reserva(2, dia=3), una_reserva(3, dia=6)]
    assert siguiente_en_cola(cola).id_reserva == 2


def test_en_empate_de_fecha_gana_el_id_menor():
    cola = [una_reserva(8, dia=3), una_reserva(4, dia=3)]
    assert siguiente_en_cola(cola).id_reserva == 4


def test_siguiente_ignora_reservas_no_pendientes():
    cola = [una_reserva(1, dia=1, estado=RESERVA_ATENDIDA),
            una_reserva(2, dia=2, estado=RESERVA_CANCELADA),
            una_reserva(3, dia=3)]
    assert siguiente_en_cola(cola).id_reserva == 3


def test_sin_pendientes_no_hay_siguiente():
    assert siguiente_en_cola([una_reserva(estado=RESERVA_ATENDIDA)]) is None


# ---------- atender_reserva / cancelar_reserva ----------

def test_atender_reserva_la_deja_atendida():
    assert atender_reserva(una_reserva()).estado == RESERVA_ATENDIDA


def test_cancelar_reserva_la_deja_cancelada():
    assert cancelar_reserva(una_reserva()).estado == RESERVA_CANCELADA


def test_solo_se_atiende_una_reserva_pendiente():
    with pytest.raises(ValueError):
        atender_reserva(una_reserva(estado=RESERVA_CANCELADA))


def test_solo_se_cancela_una_reserva_pendiente():
    with pytest.raises(ValueError):
        cancelar_reserva(una_reserva(estado=RESERVA_ATENDIDA))


def test_atender_no_modifica_la_reserva_original():
    original = una_reserva()
    atender_reserva(original)
    assert original.estado == RESERVA_PENDIENTE