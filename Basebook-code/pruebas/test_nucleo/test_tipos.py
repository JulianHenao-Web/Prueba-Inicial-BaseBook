"""Pruebas de los tipos de datos del núcleo."""
from dataclasses import FrozenInstanceError, replace
from datetime import date

import pytest

from nucleo.tipos import (
    Libro,
    Multa,
    Parametros,
    Prestamo,
    Reserva,
    Usuario,
    ESTADO_CUENTA_ACTIVA,
    LIBRO_DISPONIBLE,
    MULTA_PENDIENTE,
    PRESTAMO_SOLICITADO,
    RESERVA_PENDIENTE,
    ROL_ADMINISTRADOR,
    ROL_BIBLIOTECARIO,
    ROL_LECTOR,
    ROLES,
)


def un_usuario():
    return Usuario(
        id_usuario=1,
        nombre_completo="Ana Gómez",
        numero_identificacion="1001",
        correo="ana@correo.com",
        telefono="3001234567",
        contrasena_hash="hash",
        rol=ROL_LECTOR,
    )


def un_libro():
    return Libro(
        id_libro=1,
        isbn="978-0000000001",
        titulo="Cien años de soledad",
        autor="Gabriel García Márquez",
        categoria="Novela",
        editorial="Sudamericana",
        anio_publicacion=1967,
    )


def test_roles_disponibles():
    assert ROLES == (ROL_ADMINISTRADOR, ROL_BIBLIOTECARIO, ROL_LECTOR)


def test_usuario_nace_con_cuenta_activa():
    assert un_usuario().estado_cuenta == ESTADO_CUENTA_ACTIVA


def test_libro_nace_disponible():
    assert un_libro().estado == LIBRO_DISPONIBLE


def test_prestamo_nace_como_solicitud_sin_bibliotecario():
    prestamo = Prestamo(
        id_prestamo=1,
        id_lector=1,
        id_libro=1,
        fecha_solicitud=date(2026, 10, 20),
    )
    assert prestamo.estado == PRESTAMO_SOLICITADO
    assert prestamo.id_bibliotecario is None
    assert prestamo.fecha_prestamo is None
    assert prestamo.fecha_devolucion_real is None


def test_reserva_nace_pendiente():
    reserva = Reserva(id_reserva=1, id_lector=1, id_libro=1, fecha_reserva=date(2026, 10, 20))
    assert reserva.estado == RESERVA_PENDIENTE


def test_multa_nace_pendiente_sin_fecha_de_pago():
    multa = Multa(
        id_multa=1,
        id_prestamo=1,
        dias_retraso=3,
        valor_total=3000.0,
        fecha_generacion=date(2026, 10, 25),
    )
    assert multa.estado == MULTA_PENDIENTE
    assert multa.fecha_pago is None


def test_parametros_guardan_periodo_y_valor_de_multa():
    parametros = Parametros(periodo_prestamo_dias=15, valor_multa_por_dia=1000.0)
    assert parametros.periodo_prestamo_dias == 15
    assert parametros.valor_multa_por_dia == 1000.0


def test_los_tipos_son_inmutables():
    libro = un_libro()
    with pytest.raises(FrozenInstanceError):
        libro.estado = "prestado"


def test_replace_crea_una_copia_con_el_cambio():
    libro = un_libro()
    prestado = replace(libro, estado="prestado")
    assert prestado.estado == "prestado"
    assert libro.estado == LIBRO_DISPONIBLE  # el original no cambia