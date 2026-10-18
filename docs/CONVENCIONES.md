# Convenciones de trabajo

## Ramas

| Rama | Para qué sirve | Se crea desde | Se integra en |
|---|---|---|---|
| `main` | Versiones estables y verificadas | — | Solo recibe `develop` |
| `develop` | Integración de funcionalidades terminadas | `main` | `main` (al cerrar una fase) |
| `feature/<nombre>` | Una funcionalidad o cambio pequeño | `develop` | `develop`, mediante Pull Request |

Reglas:

- **Nunca** se hacen commits directamente en `main` ni en `develop`.
- Una rama `feature` tiene **un solo propósito** y vive poco tiempo.
- El nombre va en minúsculas y con guiones: `feature/reglas-multa`.

## Commits

Formato: `tipo(alcance): descripción en presente`

| Tipo | Se usa para |
|---|---|
| `feat` | Una funcionalidad nueva |
| `fix` | Corregir un error |
| `test` | Agregar o ajustar pruebas |
| `docs` | Documentación |
| `refactor` | Mejorar el código sin cambiar su comportamiento |
| `chore` | Configuración y tareas de mantenimiento |

Reglas:

- Máximo 72 caracteres en la primera línea.
- Un commit = un cambio lógico.
- Descripción en presente y específica: `feat(nucleo): agrega calcular_multa()`.
- Se evitan mensajes genéricos como "Update", "cambios" o "arreglos".

Ejemplos:

```
feat(nucleo): agrega dias_retraso() en reglas_multa
test(nucleo): agrega pruebas de calcular_multa()
fix(nucleo): corrige el cálculo cuando no hay retraso
docs: actualiza el README con las instrucciones de pruebas
chore: agrega .gitignore
```

## Flujo de una funcionalidad

1. `git checkout develop` y `git pull origin develop`
2. `git checkout -b feature/<nombre>`
3. Escribir las pruebas y el código, con commits pequeños.
4. Ejecutar `python -m pytest` y comprobar que todo pasa.
5. `git push -u origin feature/<nombre>`
6. Abrir un Pull Request hacia `develop`.
7. Revisión con la lista de abajo.
8. Merge a `develop` y borrar la rama `feature`.

## Lista de revisión de un Pull Request

- [ ] Hace una sola cosa y coincide con el nombre de la rama.
- [ ] Las pruebas pasan (`python -m pytest`).
- [ ] El código respeta las capas: `nucleo/` no importa Flask ni la base de datos.
- [ ] Los mensajes de commit siguen la convención.
- [ ] No se suben credenciales ni archivos `.env`.
- [ ] La bitácora del documento está actualizada.

## Definición de terminado

Una funcionalidad está terminada cuando está en `develop`, con pruebas que pasan, commits bien nombrados y su avance registrado en la documentación.
