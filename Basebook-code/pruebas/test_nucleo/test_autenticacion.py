"""Pruebas de autenticación (RF01, RF02, RNF03)."""
from dataclasses import replace

from nucleo.autenticacion import (
    cifrar_contrasena,
    puede_iniciar_sesion,
    verificar_contrasena,
)
from nucleo.tipos import ESTADO_CUENTA_INACTIVA, ROL_LECTOR, Usuario

# Pocas iteraciones en las pruebas para que corran rápido.
RAPIDO = 1000


def un_usuario(contrasena="clave1234", **cambios):
    hash_ = cifrar_contrasena(contrasena, iteraciones=RAPIDO)
    base = Usuario(1, "Ana Pérez", "100", "ana@correo.com", "300", hash_, ROL_LECTOR)
    return replace(base, **cambios)


# ---------- cifrar_contrasena ----------

def test_el_hash_no_contiene_la_contrasena():
    assert "clave1234" not in cifrar_contrasena("clave1234", iteraciones=RAPIDO)


def test_el_hash_indica_algoritmo_y_tiene_cuatro_partes():
    partes = cifrar_contrasena("clave1234", iteraciones=RAPIDO).split("$")
    assert len(partes) == 4
    assert partes[0] == "pbkdf2_sha256"
    assert partes[1] == str(RAPIDO)


def test_misma_contrasena_genera_hashes_distintos_por_la_sal():
    h1 = cifrar_contrasena("clave1234", iteraciones=RAPIDO)
    h2 = cifrar_contrasena("clave1234", iteraciones=RAPIDO)
    assert h1 != h2


def test_con_la_misma_sal_el_hash_es_igual():
    h1 = cifrar_contrasena("clave1234", sal=b"0123456789abcdef", iteraciones=RAPIDO)
    h2 = cifrar_contrasena("clave1234", sal=b"0123456789abcdef", iteraciones=RAPIDO)
    assert h1 == h2


def test_iteraciones_por_defecto_son_altas():
    assert int(cifrar_contrasena("clave1234").split("$")[1]) >= 200_000


# ---------- verificar_contrasena ----------

def test_contrasena_correcta_se_verifica():
    h = cifrar_contrasena("clave1234", iteraciones=RAPIDO)
    assert verificar_contrasena("clave1234", h) is True


def test_contrasena_incorrecta_no_se_verifica():
    h = cifrar_contrasena("clave1234", iteraciones=RAPIDO)
    assert verificar_contrasena("otra-clave", h) is False


def test_distingue_mayusculas():
    h = cifrar_contrasena("Clave1234", iteraciones=RAPIDO)
    assert verificar_contrasena("clave1234", h) is False


def test_hash_mal_formado_no_se_verifica():
    assert verificar_contrasena("clave1234", "esto-no-es-un-hash") is False


def test_hash_vacio_no_se_verifica():
    assert verificar_contrasena("clave1234", "") is False


def test_algoritmo_desconocido_no_se_verifica():
    assert verificar_contrasena("clave1234", "md5$1000$aa$bb") is False


def test_iteraciones_no_numericas_no_se_verifican():
    assert verificar_contrasena("clave1234", "pbkdf2_sha256$mil$aa$bb") is False


# ---------- puede_iniciar_sesion ----------

def test_cuenta_activa_con_contrasena_correcta_inicia_sesion():
    assert puede_iniciar_sesion(un_usuario(), "clave1234") is True


def test_contrasena_incorrecta_no_inicia_sesion():
    assert puede_iniciar_sesion(un_usuario(), "mala") is False


def test_cuenta_inactiva_no_inicia_sesion_aunque_la_clave_sea_correcta():
    usuario = un_usuario(estado_cuenta=ESTADO_CUENTA_INACTIVA)
    assert puede_iniciar_sesion(usuario, "clave1234") is False