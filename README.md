# Prueba-Inicial-BaseBook

Repositorio de **práctica** del equipo de BaseBook (Sistema de Gestión de Biblioteca). Es independiente del repositorio oficial y existe para aprender, paso a paso, a desarrollar, probar, revisar e integrar funcionalidades con Git y GitHub.

## Objetivos

- Planificar el avance del proyecto en pasos pequeños.
- Desarrollar, probar, revisar y aprobar funcionalidades.
- Usar correctamente las ramas `main`, `develop` y `feature/*`.
- Nombrar los commits de forma clara y consistente.
- Documentar el proceso de desarrollo.

## Arquitectura

Cliente-Servidor Web organizada en tres capas:

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| Presentación | `interfaz/` | Rutas web (Flask), plantillas y estáticos |
| Negocio | `nucleo/` | Reglas como funciones puras, sin depender de Flask ni de la base de datos |
| Datos | `almacen/` | Lectura y escritura en la base de datos y transacciones |

## Estructura

```
Prueba-Inicial-BaseBook/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   └── CONVENCIONES.md
└── Basebook-code/
    ├── main.py
    ├── interfaz/
    ├── nucleo/
    ├── almacen/
    ├── pruebas/
    └── datos/
```

## Cómo trabajar

El flujo de ramas, los nombres de commits y la lista de revisión están en [`docs/CONVENCIONES.md`](docs/CONVENCIONES.md).

## Cómo ejecutar las pruebas

```
pip install -r requirements.txt
cd Basebook-code
python -m pytest
```

## Estado

Fase 0: preparación del repositorio. Aún no hay funcionalidades implementadas.
