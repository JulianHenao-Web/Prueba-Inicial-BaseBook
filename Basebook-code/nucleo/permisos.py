"""Permisos por rol (RF10, RF18). Datos y funciones puras: sin Flask ni BD.

Cada operación del sistema es una constante; PERMISOS dice qué operaciones
puede realizar cada rol. Las rutas web consultan `rol_permite` antes de actuar.
"""
from nucleo.tipos import ROL_ADMINISTRADOR, ROL_BIBLIOTECARIO, ROL_LECTOR

# Operaciones del catálogo y consulta
CONSULTAR_CATALOGO = "consultar_catalogo"
BUSCAR_LIBRO = "buscar_libro"
CONSULTAR_DISPONIBILIDAD = "consultar_disponibilidad"
GESTIONAR_LIBROS = "gestionar_libros"

# Operaciones del lector
SOLICITAR_PRESTAMO = "solicitar_prestamo"
SOLICITAR_RESERVA = "solicitar_reserva"
CONSULTAR_MIS_PRESTAMOS = "consultar_mis_prestamos"
CONSULTAR_MIS_MULTAS = "consultar_mis_multas"

# Operaciones del bibliotecario
CONSULTAR_USUARIOS = "consultar_usuarios"
REGISTRAR_PRESTAMO = "registrar_prestamo"
REGISTRAR_DEVOLUCION = "registrar_devolucion"
CONSULTAR_PRESTAMOS = "consultar_prestamos"
GESTIONAR_RESERVAS = "gestionar_reservas"
GESTIONAR_MULTAS = "gestionar_multas"

# Operaciones del administrador
GESTIONAR_USUARIOS = "gestionar_usuarios"
ASIGNAR_ROLES = "asignar_roles"
CONFIGURAR_PARAMETROS = "configurar_parametros"

_CONSULTA = {CONSULTAR_CATALOGO, BUSCAR_LIBRO, CONSULTAR_DISPONIBILIDAD}

PERMISOS = {
    ROL_LECTOR: frozenset(_CONSULTA | {
        SOLICITAR_PRESTAMO,
        SOLICITAR_RESERVA,
        CONSULTAR_MIS_PRESTAMOS,
        CONSULTAR_MIS_MULTAS,
    }),
    ROL_BIBLIOTECARIO: frozenset(_CONSULTA | {
        GESTIONAR_LIBROS,
        CONSULTAR_USUARIOS,
        REGISTRAR_PRESTAMO,
        REGISTRAR_DEVOLUCION,
        CONSULTAR_PRESTAMOS,
        GESTIONAR_RESERVAS,
        GESTIONAR_MULTAS,
    }),
    ROL_ADMINISTRADOR: frozenset({
        GESTIONAR_USUARIOS,
        ASIGNAR_ROLES,
        CONFIGURAR_PARAMETROS,
    }),
}

OPERACIONES = frozenset().union(*PERMISOS.values())


def rol_permite(rol: str, operacion: str) -> bool:
    """True si el rol puede realizar la operación; rol u operación desconocidos -> False."""
    return operacion in PERMISOS.get(rol, frozenset())