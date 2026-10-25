"""Pruebas de las reglas de usuario (RF01, RF09, RF10)."""
from dataclasses import replace
from datetime import date

import pytest

from nucleo.reglas_usuario import (
    cambiar_estado_cuenta,
    cambiar_rol,
    correo_valido,
    crear_lector,
    rol_valido,
    validar_datos_registro,
)
from nucleo.tipos import (
    ESTADO_CUENTA_ACTIVA,
    ESTADO_CUENTA_INACTIVA,
    ROL_ADMINISTRADOR,
    ROL_BIBLIOTECARIO,
    ROL_LECTOR,
    Usuario,
)

DATOS_OK = dict(
    nombre_completo="Ana Pérez",
    numero_identificacion="1088000111",
    correo="ana@correo.com",
    telefono="3001234567",
    contrasena="clave1234",
)


def con(**cambios):
    return {**DATOS_OK, **cambios}


def un_usuario(**cambios):
    base = Usuario(1, "Ana Pérez", "100", "ana@correo.com", "300", "hash", ROL_LECTOR)
    return replace(base, **cambios)


# ---------- correo_valido ----------

@pytest.mark.parametrize("correo", [
    "ana@correo.com",
    "julian.henao3@utp.edu.co",
    "a_b-c+d@dominio.org",
])
def test_correos_validos(correo):
    assert correo_valido(correo) is True


@pytest.mark.parametrize("correo", [
    "",
    "sin-arroba.com",
    "@correo.com",
    "ana@",
    "ana@correo",
    "ana @correo.com",
    "ana@@correo.com",
])
def test_correos_invalidos(correo):
    assert correo_valido(correo) is False


# ---------- rol_valido ----------

@pytest.mark.parametrize("rol", [ROL_LECTOR, ROL_BIBLIOTECARIO, ROL_ADMINISTRADOR])
def test_roles_validos(rol):
    assert rol_valido(rol) is True


def test_rol_desconocido_es_invalido():
    assert rol_valido("invitado") is False


# ---------- validar_datos_registro ----------

def test_datos_completos_y_correctos_no_tienen_errores():
    assert validar_datos_registro(**DATOS_OK) == []


@pytest.mark.parametrize("campo", [
    "nombre_completo", "numero_identificacion", "correo", "telefono", "contrasena",
])
def test_campo_vacio_es_error(campo):
    errores = validar_datos_registro(**con(**{campo: ""}))
    assert len(errores) >= 1


def test_campo_solo_con_espacios_es_error():
    assert validar_datos_registro(**con(nombre_completo="   ")) != []


def test_correo_con_formato_invalido_es_error():
    errores = validar_datos_registro(**con(correo="no-es-correo"))
    assert any("correo" in e.lower() for e in errores)


def test_contrasena_corta_es_error():
    errores = validar_datos_registro(**con(contrasena="abc12"))
    assert any("contraseña" in e.lower() for e in errores)


def test_telefono_con_letras_es_error():
    errores = validar_datos_registro(**con(telefono="30012abc"))
    assert any("teléfono" in e.lower() for e in errores)


def test_varios_errores_se_reportan_juntos():
    errores = validar_datos_registro(**con(nombre_completo="", correo="x", contrasena="1"))
    assert len(errores) == 3


# ---------- crear_lector ----------

def test_crear_lector_asigna_rol_lector_y_cuenta_activa():
    u = crear_lector(
        id_usuario=9,
        nombre_completo="Ana Pérez",
        numero_identificacion="1088000111",
        correo="ana@correo.com",
        telefono="3001234567",
        contrasena="clave1234",
        contrasena_hash="HASH",
        fecha_registro=date(2026, 10, 25),
    )
    assert u.rol == ROL_LECTOR
    assert u.estado_cuenta == ESTADO_CUENTA_ACTIVA
    assert u.contrasena_hash == "HASH"
    assert u.id_usuario == 9
    assert u.fecha_registro == date(2026, 10, 25)


def test_crear_lector_no_guarda_la_contrasena_en_claro():
    u = crear_lector(9, "Ana Pérez", "1088000111", "ana@correo.com",
                     "3001234567", "clave1234", "HASH", date(2026, 10, 25))
    assert "clave1234" not in repr(u)


def test_crear_lector_con_datos_invalidos_lanza_error():
    with pytest.raises(ValueError):
        crear_lector(9, "", "1088000111", "ana@correo.com",
                     "3001234567", "clave1234", "HASH", date(2026, 10, 25))


# ---------- cambiar_rol ----------

def test_cambiar_rol_devuelve_usuario_con_nuevo_rol():
    assert cambiar_rol(un_usuario(), ROL_BIBLIOTECARIO).rol == ROL_BIBLIOTECARIO


def test_cambiar_rol_no_modifica_el_original():
    original = un_usuario()
    cambiar_rol(original, ROL_ADMINISTRADOR)
    assert original.rol == ROL_LECTOR


def test_cambiar_a_rol_invalido_lanza_error():
    with pytest.raises(ValueError):
        cambiar_rol(un_usuario(), "invitado")


# ---------- cambiar_estado_cuenta ----------

def test_desactivar_cuenta():
    u = cambiar_estado_cuenta(un_usuario(), ESTADO_CUENTA_INACTIVA)
    assert u.estado_cuenta == ESTADO_CUENTA_INACTIVA


def test_reactivar_cuenta():
    u = cambiar_estado_cuenta(un_usuario(estado_cuenta=ESTADO_CUENTA_INACTIVA),
                              ESTADO_CUENTA_ACTIVA)
    assert u.estado_cuenta == ESTADO_CUENTA_ACTIVA


def test_estado_de_cuenta_invalido_lanza_error():
    with pytest.raises(ValueError):
        cambiar_estado_cuenta(un_usuario(), "suspendida")