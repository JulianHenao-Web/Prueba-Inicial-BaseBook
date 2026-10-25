"""Pruebas de permisos por rol (RF10, RF18)."""
import pytest

from nucleo import permisos
from nucleo.permisos import PERMISOS, rol_permite
from nucleo.tipos import ROL_ADMINISTRADOR, ROL_BIBLIOTECARIO, ROL_LECTOR, ROLES


def test_todos_los_roles_tienen_permisos_definidos():
    assert set(PERMISOS) == set(ROLES)


def test_los_permisos_usan_solo_operaciones_conocidas():
    for operaciones in PERMISOS.values():
        assert operaciones <= permisos.OPERACIONES


# ---------- Lector ----------

@pytest.mark.parametrize("operacion", [
    permisos.CONSULTAR_CATALOGO,
    permisos.BUSCAR_LIBRO,
    permisos.CONSULTAR_DISPONIBILIDAD,
    permisos.SOLICITAR_PRESTAMO,
    permisos.SOLICITAR_RESERVA,
    permisos.CONSULTAR_MIS_PRESTAMOS,
    permisos.CONSULTAR_MIS_MULTAS,
])
def test_lector_puede(operacion):
    assert rol_permite(ROL_LECTOR, operacion) is True


@pytest.mark.parametrize("operacion", [
    permisos.GESTIONAR_LIBROS,
    permisos.REGISTRAR_PRESTAMO,
    permisos.REGISTRAR_DEVOLUCION,
    permisos.GESTIONAR_MULTAS,
    permisos.GESTIONAR_USUARIOS,
    permisos.CONFIGURAR_PARAMETROS,
])
def test_lector_no_puede(operacion):
    assert rol_permite(ROL_LECTOR, operacion) is False


# ---------- Bibliotecario ----------

@pytest.mark.parametrize("operacion", [
    permisos.CONSULTAR_CATALOGO,
    permisos.BUSCAR_LIBRO,
    permisos.CONSULTAR_DISPONIBILIDAD,
    permisos.GESTIONAR_LIBROS,
    permisos.CONSULTAR_USUARIOS,
    permisos.REGISTRAR_PRESTAMO,
    permisos.REGISTRAR_DEVOLUCION,
    permisos.CONSULTAR_PRESTAMOS,
    permisos.GESTIONAR_RESERVAS,
    permisos.GESTIONAR_MULTAS,
])
def test_bibliotecario_puede(operacion):
    assert rol_permite(ROL_BIBLIOTECARIO, operacion) is True


@pytest.mark.parametrize("operacion", [
    permisos.GESTIONAR_USUARIOS,
    permisos.ASIGNAR_ROLES,
    permisos.CONFIGURAR_PARAMETROS,
    permisos.SOLICITAR_PRESTAMO,
])
def test_bibliotecario_no_puede(operacion):
    assert rol_permite(ROL_BIBLIOTECARIO, operacion) is False


# ---------- Administrador (RF18: no opera catálogo, préstamos ni reservas) ----------

@pytest.mark.parametrize("operacion", [
    permisos.GESTIONAR_USUARIOS,
    permisos.ASIGNAR_ROLES,
    permisos.CONFIGURAR_PARAMETROS,
])
def test_administrador_puede(operacion):
    assert rol_permite(ROL_ADMINISTRADOR, operacion) is True


@pytest.mark.parametrize("operacion", [
    permisos.GESTIONAR_LIBROS,
    permisos.REGISTRAR_PRESTAMO,
    permisos.REGISTRAR_DEVOLUCION,
    permisos.GESTIONAR_RESERVAS,
    permisos.GESTIONAR_MULTAS,
])
def test_administrador_no_opera_catalogo_ni_prestamos(operacion):
    assert rol_permite(ROL_ADMINISTRADOR, operacion) is False


# ---------- Casos límite ----------

def test_rol_desconocido_no_tiene_permisos():
    assert rol_permite("invitado", permisos.CONSULTAR_CATALOGO) is False


def test_operacion_desconocida_no_esta_permitida():
    assert rol_permite(ROL_BIBLIOTECARIO, "borrar_la_base_de_datos") is False


def test_los_permisos_son_inmutables():
    with pytest.raises(AttributeError):
        PERMISOS[ROL_LECTOR].add(permisos.GESTIONAR_USUARIOS)