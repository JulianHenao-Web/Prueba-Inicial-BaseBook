-- Esquema de la base de datos de BaseBook (PostgreSQL / Supabase)
-- Ejecutar en el SQL Editor de Supabase. Es seguro volver a ejecutarlo:
-- borra y recrea las tablas (¡elimina los datos existentes!).

DROP TABLE IF EXISTS multas        CASCADE;
DROP TABLE IF EXISTS reservas      CASCADE;
DROP TABLE IF EXISTS prestamos     CASCADE;
DROP TABLE IF EXISTS libros        CASCADE;
DROP TABLE IF EXISTS usuarios      CASCADE;
DROP TABLE IF EXISTS parametros    CASCADE;

-- Usuarios (Lector, Bibliotecario, Administrador)
CREATE TABLE usuarios (
    id_usuario             SERIAL       PRIMARY KEY,
    nombre_completo        TEXT         NOT NULL,
    numero_identificacion  TEXT         NOT NULL UNIQUE,
    correo                 TEXT         NOT NULL UNIQUE,
    telefono               TEXT         NOT NULL,
    contrasena_hash        TEXT         NOT NULL,
    rol                    TEXT         NOT NULL
        CHECK (rol IN ('administrador', 'bibliotecario', 'lector')),
    estado_cuenta          TEXT         NOT NULL DEFAULT 'activa'
        CHECK (estado_cuenta IN ('activa', 'inactiva')),
    fecha_registro         DATE         NOT NULL DEFAULT CURRENT_DATE
);

-- Libros del catálogo
CREATE TABLE libros (
    id_libro          SERIAL   PRIMARY KEY,
    isbn              TEXT     NOT NULL UNIQUE,
    titulo            TEXT     NOT NULL,
    autor             TEXT     NOT NULL,
    categoria         TEXT     NOT NULL,
    editorial         TEXT     NOT NULL,
    anio_publicacion  INTEGER  NOT NULL CHECK (anio_publicacion > 0),
    estado            TEXT     NOT NULL DEFAULT 'disponible'
        CHECK (estado IN ('disponible', 'prestado', 'reservado')),
    fecha_registro    DATE     NOT NULL DEFAULT CURRENT_DATE
);

-- Préstamos: SOLICITADO -> ACTIVO -> DEVUELTO (o VENCIDO)
CREATE TABLE prestamos (
    id_prestamo                SERIAL  PRIMARY KEY,
    id_lector                  INTEGER NOT NULL REFERENCES usuarios (id_usuario),
    id_libro                   INTEGER NOT NULL REFERENCES libros (id_libro),
    id_bibliotecario           INTEGER REFERENCES usuarios (id_usuario),
    fecha_solicitud            DATE    NOT NULL,
    fecha_prestamo             DATE,
    fecha_prevista_devolucion  DATE,
    fecha_devolucion_real      DATE,
    estado                     TEXT    NOT NULL DEFAULT 'solicitado'
        CHECK (estado IN ('solicitado', 'activo', 'devuelto', 'vencido'))
);

-- Un libro no puede tener dos préstamos en curso a la vez (RNF04)
CREATE UNIQUE INDEX un_prestamo_en_curso_por_libro
    ON prestamos (id_libro)
    WHERE estado IN ('activo', 'vencido');

-- Reservas: PENDIENTE -> ATENDIDA o CANCELADA
CREATE TABLE reservas (
    id_reserva     SERIAL  PRIMARY KEY,
    id_lector      INTEGER NOT NULL REFERENCES usuarios (id_usuario),
    id_libro       INTEGER NOT NULL REFERENCES libros (id_libro),
    fecha_reserva  DATE    NOT NULL,
    estado         TEXT    NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'atendida', 'cancelada'))
);

-- Un lector no puede tener dos reservas pendientes del mismo libro
CREATE UNIQUE INDEX una_reserva_pendiente_por_lector_y_libro
    ON reservas (id_lector, id_libro)
    WHERE estado = 'pendiente';

-- Multas: una por préstamo devuelto con retraso (RF19)
CREATE TABLE multas (
    id_multa          SERIAL         PRIMARY KEY,
    id_prestamo       INTEGER        NOT NULL UNIQUE REFERENCES prestamos (id_prestamo),
    dias_retraso      INTEGER        NOT NULL CHECK (dias_retraso > 0),
    valor_total       NUMERIC(10, 2) NOT NULL CHECK (valor_total >= 0),
    fecha_generacion  DATE           NOT NULL,
    estado            TEXT           NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'pagada')),
    fecha_pago        DATE,
    -- una multa pagada debe tener fecha de pago, y una pendiente no (RNF04)
    CHECK ((estado = 'pagada') = (fecha_pago IS NOT NULL))
);

-- Parámetros del sistema: una sola fila (RF21)
CREATE TABLE parametros (
    id_configuracion      INTEGER        PRIMARY KEY DEFAULT 1 CHECK (id_configuracion = 1),
    periodo_prestamo_dias INTEGER        NOT NULL CHECK (periodo_prestamo_dias > 0),
    valor_multa_por_dia   NUMERIC(10, 2) NOT NULL CHECK (valor_multa_por_dia >= 0),
    fecha_actualizacion   DATE           NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO parametros (periodo_prestamo_dias, valor_multa_por_dia) VALUES (15, 1000.00);