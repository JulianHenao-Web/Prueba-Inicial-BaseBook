"""Reglas de reservas (RF15). Funciones puras: sin Flask ni BD.

Ciclo de vida de una reserva: PENDIENTE -> ATENDIDA o CANCELADA.
"""
from dataclasses import replace
from datetime import date
from typing import Iterable, Optional

from nucleo.tipos import (
    ESTADO_CUENTA_ACTIVA,
    LIBRO_DISPONIBLE,
    RESERVA_ATENDIDA,
    RESERVA_CANCELADA,
    RESERVA_PENDIENTE,
    ROL_LECTOR,
    Libro,
    Reserva,
    Usuario,
)


def puede_reservar(lector: Usuario, libro: Libro, reservas: Iterable[Reserva]) -> bool:
    """Un lector activo puede reservar un libro NO disponible si no lo tiene ya reservado.

    `reservas` son las reservas existentes (cualquier libro o lector); solo
    cuentan las pendientes del mismo lector y el mismo libro.
    """
    ya_reservado = any(
        r.id_lector == lector.id_usuario
        and r.id_libro == libro.id_libro
        and r.estado == RESERVA_PENDIENTE
        for r in reservas
    )
    return (
        lector.rol == ROL_LECTOR
        and lector.estado_cuenta == ESTADO_CUENTA_ACTIVA
        and libro.estado != LIBRO_DISPONIBLE
        and not ya_reservado
    )


def crear_reserva(id_reserva: int, lector: Usuario, libro: Libro,
                  reservas: Iterable[Reserva], fecha_reserva: date) -> Reserva:
    """Crea una reserva PENDIENTE o lanza ValueError si no se puede reservar."""
    if not puede_reservar(lector, libro, reservas):
        raise ValueError("El lector no puede reservar este libro")
    return Reserva(id_reserva, lector.id_usuario, libro.id_libro, fecha_reserva)


def siguiente_en_cola(reservas: Iterable[Reserva]) -> Optional[Reserva]:
    """Reserva pendiente más antigua (empate por id); None si no hay ninguna.

    Se asume que `reservas` son las de UN mismo libro.
    """
    pendientes = [r for r in reservas if r.estado == RESERVA_PENDIENTE]
    if not pendientes:
        return None
    return min(pendientes, key=lambda r: (r.fecha_reserva, r.id_reserva))


def atender_reserva(reserva: Reserva) -> Reserva:
    """Marca una reserva pendiente como ATENDIDA."""
    if reserva.estado != RESERVA_PENDIENTE:
        raise ValueError("Solo se puede atender una reserva pendiente")
    return replace(reserva, estado=RESERVA_ATENDIDA)


def cancelar_reserva(reserva: Reserva) -> Reserva:
    """Marca una reserva pendiente como CANCELADA."""
    if reserva.estado != RESERVA_PENDIENTE:
        raise ValueError("Solo se puede cancelar una reserva pendiente")
    return replace(reserva, estado=RESERVA_CANCELADA)