# Sprint 01 — Cierre

- **Estado:** CERRADO
- **Veredicto `@qa`:** APROBADO (sin fallas bloqueantes)
- **Fecha:** 2026-10-27
- **Especificación:** `specs/01.md`
- **Tareas:** `task[implementador].01.md`, `02.md`, `03.md`

## Alcance entregado

| Requerimiento de `specs/01.md` | Estado |
|---|---|
| Juego 2D con jugabilidad tipo Super Mario Bros | Cumplido (prototipo jugable de una pantalla) |
| Movimiento lateral | Cumplido (`A`/`←`, `D`/`→`) |
| Salto | Cumplido (`ESPACIO`/`↑`/`W`, un salto por pulsación) |
| Gravedad | Cumplido (0.8 px/frame², caída máx. 18 px/frame) |
| Colisión con el suelo | Cumplido (suelo + 3 plataformas flotantes) |
| Jugabilidad fluida | Cumplido (60 FPS con `clock.tick`, sin bloqueos) |
| Sin sprites externos | Cumplido (solo `Surface`/rectángulos y colores de `config`) |

## Entorno

- Python 3.12.14 en `.venv/`
- `pygame==2.6.1` (única dependencia, declarada en `requirements.txt`)
- Reproducible con: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt`

## Estructura final

```
requirements.txt
assets/{images,sounds,fonts}/.gitkeep
src/config.py              constantes globales (960x540, FPS, paleta, física, nivel, rutas)
src/main.py                create_level() + main() — solo Game Loop
src/entities/player.py     Player(Sprite)
src/entities/platform.py   Platform(Sprite)
src/entities/__init__.py   re-exporta Player, Platform
```

## Comandos de operación

```bash
# Ejecutar
.venv/bin/python -m src.main

# Verificación completa del sprint
.venv/bin/python -m compileall -q src
grep -rnE "time\.sleep|pygame\.time\.(wait|delay)|sys\.path|eval\(|exec\(" src/ || echo SIN_PROHIBIDOS
SDL_VIDEODRIVER=dummy .venv/bin/python -m src.main   # arranque headless
```

## Evidencia de aceptación

```
COMPILE_OK
exit=124 (bucle vivo, sin traceback)
SIN_BLOQUEOS · SIN_IMPORTS_PLANOS · SIN_DATOS_SENSIBLES · SIN_SONDA
ATERRIZAJE_OK <rect(120, 424, 40, 56)>
SIN_MURO_INVISIBLE_OK 160 frames <rect(920, 424, 40, 56)>
COLISION_LATERAL_OK <rect(480, 301, 40, 56)>
PLATAFORMA_OK <rect(300, 324, 40, 56)>
SALTO_UNICO_OK -10.999999999999996
RESPAWN_OK <rect(120, 300, 40, 56)>
TODO OK
```

## Decisiones técnicas consolidadas

1. **Paso fijo a 60 FPS** (sin delta-time) para el Sprint 01: determinista y suficiente. Si el Sprint 02 introduce scroll o enemigos, se evaluará delta-time.
2. **`main.py` sin clases**: toda la lógica vive en `entities/`; el nivel se define como datos en `config.LEVEL_PLATFORMS`.
3. **Imports absolutos** desde la raíz (`from src.config import ...`); entrada oficial `python -m src.main`.
4. **Nivel con holgura**: 76 px entre suelo y primera plataforma, salto útil ≈ 140 px, escalera 480→380→300→220.
5. **Sin assets**: se posponen a cuando `specs/` los pida; `assets/` queda preparado y las rutas ya son dinámicas con `os.path.join`.

## Deuda técnica asumida (para Sprint 02)

| # | Deuda | Impacto |
|---|---|---|
| 1 | El texto fijo del HUD se renderiza cada frame | Asignaciones innecesarias; trivial de cachear |
| 2 | Una sola pantalla, sin cámara ni scroll | Limitación de diseño, no defecto |
| 3 | Sin tests automatizados en el repo (la verificación fue por comandos) | Riesgo de regresión al añadir mecánicas |
| 4 | Sin sonido, animaciones ni enemigos | Fuera de alcance del Sprint 01 |

## Historial del ciclo

| Tarea | Resultado |
|---|---|
| 01 | Entorno y base creados; **rechazada** por desviaciones (800x600, imports planos, sin HUD, sin colisión horizontal, sin respawn, auto-salto) |
| 02 | Corrección D1–D7; aprobada en forma, pero introdujo un muro invisible con una sonda de 1 px |
| 03 | Eliminación del muro invisible, nuevo layout del nivel y Enmienda A1 al test de salto; **APROBADO por `@qa`** |

## Próximo paso

Crear `specs/02.md` con la siguiente etapa (candidatos: scroll/cámara, enemigos, animación, sonido, puntuación). Sin especificación no se abre sprint.
