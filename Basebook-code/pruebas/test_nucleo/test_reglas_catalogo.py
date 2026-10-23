"""Pruebas de las reglas del catálogo (RF07, RF08, RF14)."""
from datetime import date

from nucleo.reglas_catalogo import estado_resultante, filtrar_libros
from nucleo.tipos import (
    LIBRO_DISPONIBLE,
    LIBRO_PRESTADO,
    LIBRO_RESERVADO,
    PRESTAMO_ACTIVO,
    PRESTAMO_DEVUELTO,
    PRESTAMO_VENCIDO,
    RESERVA_ATENDIDA,
    RESERVA_PENDIENTE,
    Libro,
    Prestamo,
    Reserva,
)


def un_libro(id_libro, titulo, autor, categoria):
    return Libro(id_libro, f"isbn-{id_libro}", titulo, autor, categoria, "Editorial", 2000)


CATALOGO = [
    un_libro(1, "Cien años de soledad", "Gabriel García Márquez", "Novela"),
    un_libro(2, "El coronel no tiene quien le escriba", "Gabriel García Márquez", "Novela"),
    un_libro(3, "Clean Code", "Robert C. Martin", "Programación"),
    un_libro(4, "Introducción a Python", "Ana Torres", "Programación"),
]


def ids(libros):
    return [libro.id_libro for libro in libros]


def un_prestamo(estado):
    return Prestamo(1, 1, 1, date(2026, 10, 1), estado=estado)


def una_reserva(estado):
    return Reserva(1, 1, 1, date(2026, 10, 1), estado=estado)


# ---------- filtrar_libros ----------

def test_sin_criterios_devuelve_todo_el_catalogo():
    assert ids(filtrar_libros(CATALOGO)) == [1, 2, 3, 4]


def test_filtra_por_titulo_parcial():
    assert ids(filtrar_libros(CATALOGO, titulo="soledad")) == [1]


def test_filtra_por_autor():
    assert ids(filtrar_libros(CATALOGO, autor="Márquez")) == [1, 2]


def test_filtra_por_categoria():
    assert ids(filtrar_libros(CATALOGO, categoria="Programación")) == [3, 4]


def test_busqueda_ignora_mayusculas():
    assert ids(filtrar_libros(CATALOGO, titulo="CLEAN")) == [3]


def test_varios_criterios_se_combinan():
    assert ids(filtrar_libros(CATALOGO, autor="Márquez", titulo="coronel")) == [2]


def test_sin_coincidencias_devuelve_lista_vacia():
    assert filtrar_libros(CATALOGO, titulo="no existe") == []


def test_criterio_vacio_se_ignora():
    assert ids(filtrar_libros(CATALOGO, titulo="")) == [1, 2, 3, 4]


def test_no_modifica_la_lista_original():
    copia = list(CATALOGO)
    filtrar_libros(CATALOGO, titulo="clean")
    assert CATALOGO == copia


# ---------- estado_resultante ----------

def test_sin_prestamos_ni_reservas_esta_disponible():
    assert estado_resultante([], []) == LIBRO_DISPONIBLE


def test_con_prestamo_activo_esta_prestado():
    assert estado_resultante([un_prestamo(PRESTAMO_ACTIVO)], []) == LIBRO_PRESTADO


def test_con_prestamo_vencido_sigue_prestado():
    assert estado_resultante([un_prestamo(PRESTAMO_VENCIDO)], []) == LIBRO_PRESTADO


def test_prestamo_devuelto_no_cuenta():
    assert estado_resultante([un_prestamo(PRESTAMO_DEVUELTO)], []) == LIBRO_DISPONIBLE


def test_devuelto_con_reserva_pendiente_queda_reservado():
    assert estado_resultante(
        [un_prestamo(PRESTAMO_DEVUELTO)], [una_reserva(RESERVA_PENDIENTE)]
    ) == LIBRO_RESERVADO


def test_reserva_atendida_no_cuenta():
    assert estado_resultante([], [una_reserva(RESERVA_ATENDIDA)]) == LIBRO_DISPONIBLE


def test_prestamo_activo_tiene_prioridad_sobre_la_reserva():
    assert estado_resultante(
        [un_prestamo(PRESTAMO_ACTIVO)], [una_reserva(RESERVA_PENDIENTE)]
    ) == LIBRO_PRESTADO