"""Reglas de préstamos (RF11, RF12, RF13). Funciones puras: sin Flask ni BD.

Ciclo de vida de un préstamo: SOLICITADO -> ACTIVO -> DEVUELTO.
Las funciones no modifican los objetos recibidos: devuelven copias nuevas.
"""
from dataclasses import replace
from datetime import date, timedelta

from nucleo.tipos import (
    ESTADO_CUENTA_ACTIVA,
    LIBRO_DISPONIBLE,
    PRESTAMO_ACTIVO,
    PRESTAMO_DEVUELTO,
    PRESTAMO_SOLICITADO,
    PRESTAMO_VENCIDO,
    ROL_LECTOR,
    Libro,
    Parametros,
    Prestamo,
    Usuario,
)


def puede_solicitar_prestamo(lector: Usuario, libro: Libro) -> bool:
    """Un lector con cuenta activa puede solicitar un libro disponible."""
    return (
        lector.rol == ROL_LECTOR
        and lector.estado_cuenta == ESTADO_CUENTA_ACTIVA
        and libro.estado == LIBRO_DISPONIBLE
    )


def crear_solicitud(id_prestamo: int, lector: Usuario, libro: Libro, fecha_solicitud: date) -> Prestamo:
    """Crea la solicitud de préstamo (estado SOLICITADO)."""
    if not puede_solicitar_prestamo(lector, libro):
        raise ValueError("El lector no puede solicitar este libro")
    return Prestamo(
        id_prestamo=id_prestamo,
        id_lector=lector.id_usuario,
        id_libro=libro.id_libro,
        fecha_solicitud=fecha_solicitud,
    )


def registrar_prestamo(solicitud: Prestamo, id_bibliotecario: int, fecha_prestamo: date, parametros: Parametros) -> Prestamo:
    """El bibliotecario formaliza una solicitud: pasa a ACTIVO con fechas."""
    if solicitud.estado != PRESTAMO_SOLICITADO:
        raise ValueError("Solo se puede registrar un préstamo solicitado")
    return replace(
        solicitud,
        id_bibliotecario=id_bibliotecario,
        fecha_prestamo=fecha_prestamo,
        fecha_prevista_devolucion=fecha_prestamo + timedelta(days=parametros.periodo_prestamo_dias),
        estado=PRESTAMO_ACTIVO,
    )


def cerrar_prestamo(prestamo: Prestamo, fecha_devolucion: date) -> Prestamo:
    """Registra la devolución: el préstamo pasa a DEVUELTO."""
    if prestamo.estado not in (PRESTAMO_ACTIVO, PRESTAMO_VENCIDO):
        raise ValueError("Solo se puede devolver un préstamo activo o vencido")
    return replace(prestamo, fecha_devolucion_real=fecha_devolucion, estado=PRESTAMO_DEVUELTO)