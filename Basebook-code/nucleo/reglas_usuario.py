"""Reglas de usuarios (RF01, RF09, RF10). Funciones puras: sin Flask ni BD.

Valida los datos de registro, crea cuentas de Lector y cambia rol o estado.
El cifrado de la contraseña NO está aquí: lo hace nucleo/autenticacion.py.
Estas funciones reciben el hash ya calculado.
"""
import re
from dataclasses import replace
from datetime import date
from typing import List

from nucleo.tipos import (
    ESTADO_CUENTA_ACTIVA,
    ESTADO_CUENTA_INACTIVA,
    ROL_LECTOR,
    ROLES,
    Usuario,
)

LONGITUD_MINIMA_CONTRASENA = 8
_PATRON_CORREO = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(\.[A-Za-z0-9\-]+)+$")
_PATRON_TELEFONO = re.compile(r"^\+?\d{7,15}$")
_ESTADOS_CUENTA = (ESTADO_CUENTA_ACTIVA, ESTADO_CUENTA_INACTIVA)


def correo_valido(correo: str) -> bool:
    """Formato básico de correo: texto@dominio.extensión, sin espacios."""
    return bool(_PATRON_CORREO.match(correo))


def rol_valido(rol: str) -> bool:
    return rol in ROLES


def validar_datos_registro(nombre_completo: str, numero_identificacion: str,
                           correo: str, telefono: str, contrasena: str) -> List[str]:
    """Devuelve la lista de errores encontrados (vacía si los datos son correctos)."""
    errores = []
    if not nombre_completo.strip():
        errores.append("El nombre completo es obligatorio")
    if not numero_identificacion.strip():
        errores.append("El número de identificación es obligatorio")
    if not correo.strip():
        errores.append("El correo es obligatorio")
    elif not correo_valido(correo):
        errores.append("El correo no tiene un formato válido")
    if not telefono.strip():
        errores.append("El teléfono es obligatorio")
    elif not _PATRON_TELEFONO.match(telefono):
        errores.append("El teléfono debe tener entre 7 y 15 dígitos")
    if not contrasena:
        errores.append("La contraseña es obligatoria")
    elif len(contrasena) < LONGITUD_MINIMA_CONTRASENA:
        errores.append(
            f"La contraseña debe tener al menos {LONGITUD_MINIMA_CONTRASENA} caracteres"
        )
    return errores


def crear_lector(id_usuario: int, nombre_completo: str, numero_identificacion: str,
                 correo: str, telefono: str, contrasena: str, contrasena_hash: str,
                 fecha_registro: date) -> Usuario:
    """Crea una cuenta de Lector activa; lanza ValueError si los datos no son válidos.

    `contrasena` solo se usa para validarla; en el Usuario se guarda `contrasena_hash`.
    """
    errores = validar_datos_registro(
        nombre_completo, numero_identificacion, correo, telefono, contrasena
    )
    if errores:
        raise ValueError("; ".join(errores))
    return Usuario(
        id_usuario=id_usuario,
        nombre_completo=nombre_completo.strip(),
        numero_identificacion=numero_identificacion.strip(),
        correo=correo.strip(),
        telefono=telefono.strip(),
        contrasena_hash=contrasena_hash,
        rol=ROL_LECTOR,
        estado_cuenta=ESTADO_CUENTA_ACTIVA,
        fecha_registro=fecha_registro,
    )


def cambiar_rol(usuario: Usuario, nuevo_rol: str) -> Usuario:
    """Copia del usuario con otro rol (RF10); lanza ValueError si el rol no existe."""
    if not rol_valido(nuevo_rol):
        raise ValueError(f"Rol no válido: {nuevo_rol}")
    return replace(usuario, rol=nuevo_rol)


def cambiar_estado_cuenta(usuario: Usuario, nuevo_estado: str) -> Usuario:
    """Copia del usuario con la cuenta activa o inactiva (RF09)."""
    if nuevo_estado not in _ESTADOS_CUENTA:
        raise ValueError(f"Estado de cuenta no válido: {nuevo_estado}")
    return replace(usuario, estado_cuenta=nuevo_estado)