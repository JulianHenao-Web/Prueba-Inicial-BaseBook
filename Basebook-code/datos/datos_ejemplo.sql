-- Datos de ejemplo para DESARROLLO y pruebas. No usar en producción.
-- Ejecutar DESPUÉS de esquema.sql.
-- Todos los usuarios tienen la contraseña de ejemplo: Clave12345
-- (las contraseñas se guardan cifradas, ver nucleo/autenticacion.py).

INSERT INTO usuarios (id_usuario, nombre_completo, numero_identificacion, correo, telefono, contrasena_hash, rol, fecha_registro) VALUES
(1, 'Carlos Admin',      '1000000001', 'admin@basebook.test',  '3000000001', 'pbkdf2_sha256$200000$d79b724eed59b762e2c115784909f319$b45ae67a82ab485a79e2c52ad15987786d0aeb4cad3933a1a326e3fe778ca98f', 'administrador', '2026-08-01'),
(2, 'Marta Bibliotecaria','1000000002', 'biblio@basebook.test', '3000000002', 'pbkdf2_sha256$200000$505193105b0f9282e91d29d512e483f2$b1831c45282311da7b8a2c02bf98dd5aa6d3b2804a4cb35c424946dcb6ae2776', 'bibliotecario', '2026-08-01'),
(3, 'Ana Pérez',         '1000000003', 'ana@basebook.test',    '3000000003', 'pbkdf2_sha256$200000$a22cda0c88bc609cc063c5b021875a5f$fae3c17c15781cae64bea162356d1aff67da55cc561fe9e43b35e76b4fb265dd', 'lector', '2026-08-15'),
(4, 'Luis Gómez',        '1000000004', 'luis@basebook.test',   '3000000004', 'pbkdf2_sha256$200000$a22cda0c88bc609cc063c5b021875a5f$fae3c17c15781cae64bea162356d1aff67da55cc561fe9e43b35e76b4fb265dd', 'lector', '2026-08-20');

-- El estado de cada libro es coherente con sus préstamos y reservas (ver estado_resultante)
INSERT INTO libros (id_libro, isbn, titulo, autor, categoria, editorial, anio_publicacion, estado) VALUES
(1, '978-0-00-000001-1', 'Cien años de soledad',            'Gabriel García Márquez', 'Novela',       'Sudamericana',  1967, 'disponible'),
(2, '978-0-00-000002-8', 'Clean Code',                      'Robert C. Martin',       'Programación', 'Prentice Hall', 2008, 'prestado'),
(3, '978-0-00-000003-5', 'El coronel no tiene quien le escriba', 'Gabriel García Márquez', 'Novela',  'Sudamericana',  1961, 'reservado'),
(4, '978-0-00-000004-2', 'Introducción a Python',           'Ana Torres',             'Programación', 'Alfaomega',     2020, 'disponible'),
(5, '978-0-00-000005-9', 'Estructuras de datos',            'Luis Ramírez',           'Programación', 'McGraw-Hill',   2015, 'prestado'),
(6, '978-0-00-000006-6', 'Historia de Colombia',            'Jorge Orlando Melo',     'Historia',     'Planeta',       2017, 'disponible');

INSERT INTO prestamos (id_prestamo, id_lector, id_libro, id_bibliotecario, fecha_solicitud, fecha_prestamo, fecha_prevista_devolucion, fecha_devolucion_real, estado) VALUES
(1, 3, 2, 2, '2026-10-20', '2026-10-21', '2026-11-05', NULL,         'activo'),
(2, 4, 3, 2, '2026-10-01', '2026-10-02', '2026-10-17', '2026-10-16', 'devuelto'),
(3, 3, 4, 2, '2026-09-01', '2026-09-02', '2026-09-17', '2026-09-20', 'devuelto'),
(4, 4, 5, 2, '2026-10-05', '2026-10-06', '2026-10-21', NULL,         'vencido');

INSERT INTO reservas (id_reserva, id_lector, id_libro, fecha_reserva, estado) VALUES
(1, 3, 3, '2026-10-10', 'pendiente');

-- Préstamo 3 devuelto con 3 días de retraso: 3 x 1000
INSERT INTO multas (id_multa, id_prestamo, dias_retraso, valor_total, fecha_generacion, estado, fecha_pago) VALUES
(1, 3, 3, 3000.00, '2026-09-20', 'pagada', '2026-09-21');

-- Ajusta los contadores para que los próximos INSERT no choquen con los ids de ejemplo
SELECT setval('usuarios_id_usuario_seq',  (SELECT MAX(id_usuario)  FROM usuarios));
SELECT setval('libros_id_libro_seq',      (SELECT MAX(id_libro)    FROM libros));
SELECT setval('prestamos_id_prestamo_seq',(SELECT MAX(id_prestamo) FROM prestamos));
SELECT setval('reservas_id_reserva_seq',  (SELECT MAX(id_reserva)  FROM reservas));
SELECT setval('multas_id_multa_seq',      (SELECT MAX(id_multa)    FROM multas));