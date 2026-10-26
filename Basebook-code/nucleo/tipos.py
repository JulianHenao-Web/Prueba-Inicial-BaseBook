"""Tipos de datos del núcleo (capa de Negocio).

Solo contiene los datos: clases inmutables y constantes. No tiene lógica del negocio.
Las reglas viven en los archivos reglas_*.py.
"""
from dataclasses import dataclass
from datetime import date
from typing import Optional

# --- Roles ---
ROL_ADMINISTRADOR = "administrador"
ROL_BIBLIOTECARIO = "bibliotecario"
ROL_LECTOR = "lector"
ROLES = (ROL_ADMINISTRADOR, ROL_BIBLIOTECARIO, ROL_LECTOR)

# --- Estados ---
ESTADO_CUENTA_ACTIVA = "activa"
ESTADO_CUENTA_INACTIVA = "inactiva"

LIBRO_DISPONIBLE = "disponible"
LIBRO_PRESTADO = "prestado"
LIBRO_RESERVADO = "reservado"

PRESTAMO_SOLICITADO = "solicitado"
PRESTAMO_ACTIVO = "activo"
PRESTAMO_DEVUELTO = "devuelto"
PRESTAMO_VENCIDO = "vencido"

RESERVA_PENDIENTE = "pendiente"
RESERVA_ATENDIDA = "atendida"
RESERVA_CANCELADA = "cancelada"

MULTA_PENDIENTE = "pendiente"
MULTA_PAGADA = "pagada"


@dataclass(frozen=True)
class Usuario:
    id_usuario: int
    nombre_completo: str
    numero_identificacion: str
    correo: str
    telefono: str
    contrasena_hash: str
    rol: str
    estado_cuenta: str = ESTADO_CUENTA_ACTIVA
    fecha_registro: Optional[date] = None


@dataclass(frozen=True)
class Libro:
    id_libro: int
    isbn: str
    titulo: str
    autor: str
    categoria: str
    editorial: str
    anio_publicacion: int
    estado: str = LIBRO_DISPONIBLE
    fecha_registro: Optional[date] = None


@dataclass(frozen=True)
class Prestamo:
    id_prestamo: int
    id_lector: int
    id_libro: int
    fecha_solicitud: date
    id_bibliotecario: Optional[int] = None  # 0..1: se asigna al registrar el préstamo
    fecha_prestamo: Optional[date] = None
    fecha_prevista_devolucion: Optional[date] = None
    fecha_devolucion_real: Optional[date] = None
    estado: str = PRESTAMO_SOLICITADO


@dataclass(frozen=True)
class Reserva:
    id_reserva: int
    id_lector: int
    id_libro: int
    fecha_reserva: date
    estado: str = RESERVA_PENDIENTE


@dataclass(frozen=True)
class Multa:
    id_multa: int
    id_prestamo: int
    dias_retraso: int
    valor_total: float
    fecha_generacion: date
    estado: str = MULTA_PENDIENTE
    fecha_pago: Optional[date] = None


@dataclass(frozen=True)
class Parametros:
    """Configuración general del sistema (clase ConfiguracionSistema del diagrama)."""
    periodo_prestamo_dias: int
    valor_multa_por_dia: float
    id_configuracion: int = 1
    fecha_actualizacion: Optional[date] = None