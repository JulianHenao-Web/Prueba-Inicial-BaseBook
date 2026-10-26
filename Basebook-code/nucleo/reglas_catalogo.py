"""Reglas del catálogo (RF07, RF08, RF14)."""
from typing import Iterable, List, Optional

from nucleo.tipos import (
    LIBRO_DISPONIBLE,
    LIBRO_PRESTADO,
    LIBRO_RESERVADO,
    PRESTAMO_ACTIVO,
    PRESTAMO_VENCIDO,
    RESERVA_PENDIENTE,
    Libro,
    Prestamo,
    Reserva,
)


def _coincide(texto_libro: str, criterio: Optional[str]) -> bool:
    """Un criterio vacío o None no filtra; si existe, busca sin distinguir mayúsculas."""
    if not criterio:
        return True
    return criterio.casefold() in texto_libro.casefold()


def filtrar_libros(libros: Iterable[Libro], titulo: Optional[str] = None,
                   autor: Optional[str] = None,
                   categoria: Optional[str] = None) -> List[Libro]:
    """Libros que cumplen TODOS los criterios dados (búsqueda parcial)."""
    return [
        libro for libro in libros
        if _coincide(libro.titulo, titulo)
        and _coincide(libro.autor, autor)
        and _coincide(libro.categoria, categoria)
    ]


def estado_resultante(prestamos: Iterable[Prestamo], reservas: Iterable[Reserva]) -> str:
    """Estado de un libro según SUS préstamos y reservas.

    Prestado si tiene un préstamo activo o vencido; si no, reservado si hay una
    reserva pendiente; si no, disponible.
    """
    if any(p.estado in (PRESTAMO_ACTIVO, PRESTAMO_VENCIDO) for p in prestamos):
        return LIBRO_PRESTADO
    if any(r.estado == RESERVA_PENDIENTE for r in reservas):
        return LIBRO_RESERVADO
    return LIBRO_DISPONIBLE