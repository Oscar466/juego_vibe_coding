# Task 01 — [implementador] Bootstrap del proyecto + código base del Sprint 01

| Campo | Valor |
|---|---|
| **ID de tarea** | `task[implementador].01` |
| **Sprint** | 01 (`specs/01.md`) |
| **Agente destino** | `@implementador` |
| **Emitida por** | `@leader` |
| **Depende de** | Ninguna (primera tarea del proyecto) |
| **Entregable** | Reporte de ejecución (en el chat) + código en disco |
| **Auditoría posterior** | `@qa` |
| **Estado** | cerrada — APROBADO por `@qa` (ver `tasks/sprint-01-cierre.md`) |

---

## 0. Lectura obligatoria antes de escribir una sola línea

1. `AGENTS.md` (reglas globales del proyecto).
2. `specs/01.md` (requerimiento del sprint).
3. Este archivo completo.

Si algo en este documento contradice `AGENTS.md`, **detente y notifica a `@leader`**; no improvises.

---

## 1. Objetivo

Dejar el proyecto listo para desarrollar el Sprint 01:

1. Entorno virtual `.venv` operativo con **Pygame** como única dependencia externa.
2. Estructura de directorios `src/` y `assets/` creada y versionable.
3. Código base modular en Pygame que implemente la jugabilidad mínima del sprint: **movimiento lateral, salto, gravedad y colisión con el suelo**.

Todo el arte debe construirse con primitivas de Pygame (`Surface`, `Rect`, colores sólidos). **No se usan sprites ni archivos multimedia externos en este sprint.**

---

## 2. Contexto normativo (extracto vinculante)

De `AGENTS.md`:

- Python 3.10+ con **Type Hints obligatorios en todo el código** (firmas, atributos y retornos).
- **PEP 8** estricto.
- **OOP** con separación estricta de responsabilidades:
  - `src/main.py`: **solo** el *Game Loop* (inicialización, eventos, actualización, dibujado).
  - `src/entities/`: toda entidad hereda de `pygame.sprite.Sprite`.
  - `src/config.py`: **único** lugar para variables globales (pantalla, FPS, paleta, física).
- Assets en `assets/` y cargados con rutas **relativas dinámicas** (`os.path.join`), **nunca** absolutas.
- Imágenes (cuando existan) deben cargarse con `convert()` o `convert_alpha()`.
- Cada clase y cada método complejo debe estar documentado.

De `specs/01.md`:

- Juego 2D tipo "Super Mario Bros" en su jugabilidad básica: movimiento lateral, salto, gravedad y colisión con el suelo.
- Jugabilidad fluida y sencilla.
- Sin sprites externos: solo cuadrados, rectángulos y colores sólidos.

---

## 3. Reglas de seguridad (obligatorias, no negociables)

1. **Cero credenciales codificadas en duro.** No escribir usuarios, contraseñas, tokens, API keys ni rutas con datos personales en ningún archivo.
2. **Cero operaciones de archivo inseguras.** No abrir, escribir, mover ni borrar archivos fuera de las rutas autorizadas de la sección 4. No usar `eval`, `exec`, `pickle`, `os.system` ni `subprocess` con entrada no confiable.
3. **Cero dependencias extra.** Solo `pygame` (versión fijada en la sección 5). Prohibido `pygame-ce`, `numpy`, `pyglet`, etc., salvo autorización explícita del humano.
4. **Cero accesos a red** durante la ejecución del juego.
5. Si un comando falla y la solución implica salir de estas reglas, **detente y pregunta al humano** (`ask_user`).

---

## 4. Rutas autorizadas para esta tarea

Autorización explícita del humano para crear/editar **únicamente** dentro de:

```
/home/oscar/Escritorio/juego_harness/
├── .venv/                 (creado por python3.12 -m venv)
├── requirements.txt       (nuevo)
├── src/                   (nuevo)
└── assets/                (nuevo)
```

Prohibido tocar `specs/`, `tasks/`, `.opencode/`, `AGENTS.md` o cualquier ruta fuera del proyecto.
Prohibido crear archivos **no listados** en la sección 6 (nada de `.gitignore`, `README.md`, `docs/`, `tests/`, `build/`, etc.).

---

## 5. Fase A — Entorno virtual

Ejecutar desde la raíz del proyecto:

```bash
cd /home/oscar/Escritorio/juego_harness
```

### A.1 Verificar intérprete

El sistema tiene Python **3.14** por defecto, pero Pygame puede no tener *wheels* para esa versión. **Usa Python 3.12**, que ya está verificado como compatible con `pygame==2.6.1` en esta máquina.

```bash
python3.12 --version    # debe reportar Python 3.12.x
```

Si `python3.12` no existe, **detente** y reporta a `@leader`; no instales nada a nivel de sistema.

### A.2 Crear y activar el entorno

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
```

> No es necesario "activar" el venv en los comandos: usa siempre la ruta explícita `.venv/bin/python` y `.venv/bin/pip` para evitar ambigüedad.

### A.3 Crear `requirements.txt` (contenido exacto, una sola línea)

```
pygame==2.6.1
```

Sin comentarios, sin *hashes*, sin dependencias adicionales.

### A.4 Instalar y verificar

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/python -c "import pygame, sys; print(sys.version.split()[0], pygame.version.ver)"
```

Salida esperada (aproximada):

```
3.12.x 2.6.1
```

El mensaje `Hello from the pygame community` es normal. Si la instalación falla por red o compilación, **no** cambies de librería: reporta el error.

---

## 6. Fase B — Estructura de directorios

Crear **exactamente** este árbol (nada más, nada menos):

```
juego_harness/
├── .venv/                       # generado en Fase A (no editar a mano)
├── requirements.txt             # Fase A
├── assets/
│   ├── images/.gitkeep          # archivo vacío
│   ├── sounds/.gitkeep          # archivo vacío
│   └── fonts/.gitkeep           # archivo vacío
└── src/
    ├── __init__.py              # archivo vacío
    ├── main.py
    ├── config.py
    └── entities/
        ├── __init__.py          # archivo vacío
        ├── player.py
        └── platform.py
```

Comandos sugeridos:

```bash
mkdir -p assets/images assets/sounds assets/fonts src/entities
touch assets/images/.gitkeep assets/sounds/.gitkeep assets/fonts/.gitkeep
touch src/__init__.py src/entities/__init__.py
```

Los `.gitkeep` permiten versionar carpetas vacías; **no** son assets y no deben cargarse desde código.

---

## 7. Fase C — Código base (contratos exactos)

Reglas transversales para todos los archivos:

- Type hints en **todas** las funciones, métodos, parámetros y atributos de instancia.
- Docstring de módulo y docstring en cada clase y en cada método no trivial.
- PEP 8: 4 espacios, `snake_case` para funciones/variables, `PascalCase` para clases, líneas ≤ 79–100 caracteres, imports ordenados (stdlib → third-party → locales) y separados por línea en blanco.
- Sin `print()` dentro del bucle de juego (nada de logging por frame; afecta el rendimiento).
- Sin `time.sleep()` en ninguna parte. La cadencia la controla `pygame.time.Clock.tick(FPS)`.

### 7.1 `src/config.py`

Único punto de verdad de constantes. Contenido exigido:

| Constante | Tipo | Valor |
|---|---|---|
| `ANCHO_PANTALLA` | `int` | `800` |
| `ALTO_PANTALLA` | `int` | `600` |
| `FPS` | `int` | `60` |
| `TITULO_VENTANA` | `str` | `"Sprint 01 - Plataformas"` |
| `COLOR_FONDO` | `tuple[int, int, int]` | `(107, 170, 240)` (cielo) |
| `COLOR_SUELO` | `tuple[int, int, int]` | `(94, 62, 32)` |
| `COLOR_PLATAFORMA` | `tuple[int, int, int]` | `(139, 90, 43)` |
| `COLOR_JUGADOR` | `tuple[int, int, int]` | `(220, 40, 40)` |
| `COLOR_TEXTO` | `tuple[int, int, int]` | `(255, 255, 255)` |
| `GRAVEDAD` | `float` | `0.8` (px/frame² a 60 FPS) |
| `VELOCIDAD_CAMINATA` | `float` | `5.0` (px/frame) |
| `IMPULSO_SALTO` | `float` | `-15.0` (negativo = hacia arriba) |
| `VELOCIDAD_MAXIMA_CAIDA` | `float` | `18.0` (px/frame) |
| `ALTURA_SUELO` | `int` | `80` (px) |
| `ANCHO_JUGADOR` | `int` | `40` (px) |
| `ALTO_JUGADOR` | `int` | `60` (px) |
| `RUTA_RAIZ` | `str` | ruta absoluta calculada del proyecto |
| `RUTA_ASSETS` | `str` | `os.path.join(RUTA_RAIZ, "assets")` |

Cálculo de `RUTA_RAIZ` (este archivo vive en `src/`, por lo que la raíz es su directorio padre):

```python
RUTA_RAIZ: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

Prohibido en este archivo: `pygame` (no debe importarse), lógica de juego, valores "mágicos" duplicados.

### 7.2 `src/entities/platform.py`

```python
class Platform(pygame.sprite.Sprite):
    """Cuerpo estático (suelo o plataforma)."""

    def __init__(self, x: int, y: int, ancho: int, alto: int,
                 color: tuple[int, int, int]) -> None: ...
```

Requisitos:

- Hereda de `pygame.sprite.Sprite` y llama a `super().__init__()`.
- Crea `self.image = pygame.Surface((ancho, alto))`, la pinta con `fill(color)` y aplica `.convert()` (obligatorio por regla de optimización de `AGENTS.md`).
- Define `self.rect = self.image.get_rect(topleft=(x, y))`.
- No tiene `update()` (es estático) o, si lo define, no altera su posición.
- Docstring que explique que representa suelo y plataformas flotantes.

Además, en el **mismo archivo**, la factoría del nivel inicial:

```python
def crear_plataformas_iniciales() -> pygame.sprite.Group:
    """Devuelve el grupo con el suelo y las plataformas del nivel 1."""
```

Debe devolver un `pygame.sprite.Group` con **exactamente** estas 4 plataformas:

1. Suelo: `x=0`, `y=ALTO_PANTALLA - ALTURA_SUELO`, ancho `ANCHO_PANTALLA`, alto `ALTURA_SUELO`, color `COLOR_SUELO`.
2. Plataforma: `x=180`, `y=430`, `160x24`, color `COLOR_PLATAFORMA`.
3. Plataforma: `x=430`, `y=330`, `180x24`, color `COLOR_PLATAFORMA`.
4. Plataforma: `x=680`, `y=250`, `120x24`, color `COLOR_PLATAFORMA`.

### 7.3 `src/entities/player.py`

```python
class Player(pygame.sprite.Sprite):
    """Jugador controlable con física de plataformas."""

    def __init__(self, x: int, y: int) -> None: ...

    def update(self, teclas: pygame.key.ScancodeWrapper,
               plataformas: pygame.sprite.Group) -> None: ...
```

Atributos de instancia exigidos (con type hints en el cuerpo o en `__init__`):

- `self.image: pygame.Surface` — superficie de `ANCHO_JUGADOR` x `ALTO_JUGADOR` rellena con `COLOR_JUGADOR`, con `.convert()` aplicado.
- `self.rect: pygame.Rect` — posicionado en `(x, y)`.
- `self.velocidad: pygame.math.Vector2` — inicia en `(0.0, 0.0)`.
- `self.en_suelo: bool` — inicia en `False`.

Métodos privados exigidos y su responsabilidad:

| Método | Contrato |
|---|---|
| `_mover_horizontal(self, teclas) -> None` | `K_LEFT`/`K_a` → `velocidad.x = -VELOCIDAD_CAMINATA`; `K_RIGHT`/`K_d` → `+VELOCIDAD_CAMINATA`; sin tecla → `0.0`. Suma `velocidad.x` a `self.rect.x` y luego **limita** el rect a `[0, ANCHO_PANTALLA - ancho]` para que no salga de pantalla. |
| `_procesar_salto(self, teclas) -> None` | Solo si `self.en_suelo` y se pulsa `K_SPACE`, `K_UP` o `K_w`: `velocidad.y = IMPULSO_SALTO` y `en_suelo = False`. **Sin doble salto.** |
| `_aplicar_gravedad(self) -> None` | `velocidad.y = min(velocidad.y + GRAVEDAD, VELOCIDAD_MAXIMA_CAIDA)`. |
| `_resolver_colisiones(self, plataformas) -> None` | Ver algoritmo abajo. |

Algoritmo obligatorio de `update()` (en este orden):

1. `_mover_horizontal(teclas)`
2. `_procesar_salto(teclas)`
3. `_aplicar_gravedad()`
4. `self.rect.y += int(round(self.velocidad.y))`
5. `_resolver_colisiones(plataformas)`

`_resolver_colisiones`:

- Asumir `en_suelo = False` al entrar y usar `pygame.sprite.spritecollide(self, plataformas, False)`.
- Si `velocidad.y > 0` (cayendo): apoyar al jugador con `self.rect.bottom = plataforma.rect.top`, `velocidad.y = 0.0` y `en_suelo = True`.
- Si `velocidad.y < 0` (subiendo y golpea por debajo): `self.rect.top = plataforma.rect.bottom` y `velocidad.y = 0.0`.
- El orden de resolución debe ser determinista (recorrer la lista de colisiones en orden).
- No debe haber "temblor" ni hundimiento: tras resolverse, el jugador no debe quedar solapado con la plataforma.

### 7.4 `src/main.py`

**Solo** Game Loop. Estructura exigida:

```python
class Juego:
    """Orquesta el ciclo de vida de la partida (init, eventos, update, draw)."""

    def __init__(self) -> None: ...
    def _procesar_eventos(self) -> bool: ...   # False = salir
    def _actualizar(self) -> None: ...
    def _dibujar(self) -> None: ...
    def ejecutar(self) -> None: ...


def main() -> None:
    """Punto de entrada del juego."""
    Juego().ejecutar()


if __name__ == "__main__":
    main()
```

Requisitos:

- `__init__`: `pygame.init()`, `pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))`, `pygame.display.set_caption(TITULO_VENTANA)`, `self.reloj = pygame.time.Clock()`, `self.pantalla`, `self.plataformas = crear_plataformas_iniciales()`, `self.jugador = Player(...)` dentro de un `pygame.sprite.GroupSingle` o de un `pygame.sprite.Group`, `self.ejecutando = True`.
- Posición inicial del jugador: `x = 64`, `y = ALTO_PANTALLA - ALTURA_SUELO - ALTO_JUGADOR` (apoyado sobre el suelo; `en_suelo` arranca en `False` y se corrige en el primer `update()`).
- `_procesar_eventos`: recorrer `pygame.event.get()`; `pygame.QUIT` o `K_ESCAPE` → devolver `False`.
- `_actualizar`: leer `pygame.key.get_pressed()` una sola vez por frame y llamar a `self.jugador.update(teclas, self.plataformas)`.
- `_dibujar`: `self.pantalla.fill(COLOR_FONDO)`, dibujar `self.plataformas`, dibujar el grupo del jugador y `pygame.display.flip()`.
- `ejecutar`: bucle `while self.ejecutando:` → eventos → actualizar → dibujar → `self.reloj.tick(FPS)` como **única** forma de limitar la velocidad; al salir, `pygame.quit()`.
- **Prohibido** en `main.py`: constantes numéricas de física, cálculos de colisión, lógica de movimiento, `time.sleep()`, bucles anidados bloqueantes.
- Importes internos: `from config import ...` y `from entities.player import Player`. El punto de entrada oficial es `python src/main.py` ejecutado desde la raíz (Python añade `src/` al `sys.path`). No agregues manipulación de `sys.path` ni flags de línea de comandos.

### 7.5 `src/__init__.py` y `src/entities/__init__.py`

Archivos vacíos (0 bytes). No exportar nada.

---

## 8. Mecánicas exactas del Sprint 01 (criterio funcional)

| Mecánica | Comportamiento esperado |
|---|---|
| Movimiento lateral | Flechas izquierda/derecha o `A`/`D`; velocidad constante `VELOCIDAD_CAMINATA`; se detiene al soltar. |
| Salto | `Espacio`, flecha arriba o `W`; solo con `en_suelo == True`; altura determinada por `IMPULSO_SALTO` y `GRAVEDAD`. |
| Gravedad | Aplicada cada frame; caída limitada por `VELOCIDAD_MAXIMA_CAIDA`. |
| Colisión con suelo | El jugador se apoya sobre el suelo y las 3 plataformas; no las atraviesa al caer ni al saltar desde abajo. |
| Límites de pantalla | El jugador no sale por izquierda ni derecha. |
| Fluidez | 60 FPS estables; sin `time.sleep()`; sin parpadeos (un solo `flip()` por frame). |
| Cierre | Ventana (X) o `ESC` cierran limpio, sin excepciones ni procesos colgados. |

---

## 9. Verificación obligatoria antes de entregar

Ejecutar **todos** los comandos desde `/home/oscar/Escritorio/juego_harness` y adjuntar la salida real en el reporte.

**9.1 Versión instalada**

```bash
.venv/bin/python -c "import pygame, sys; print(sys.version.split()[0], pygame.version.ver)"
```

**9.2 Sintaxis/compilación**

```bash
.venv/bin/python -m compileall -q src && echo "COMPILE OK"
```

**9.3 Arranque real (headless, sin abrir ventana)**

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 5 .venv/bin/python src/main.py; echo "exit=$?"
```

Interpretación: `exit=124` significa que el juego **se mantuvo corriendo** los 5 segundos (correcto). Cualquier otro código, o un traceback, es **fallo**.

**9.4 Prueba de física (sin crear archivos temporales)**

```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python - <<'EOF'
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
import pygame
from config import ALTO_PANTALLA, ALTURA_SUELO, ALTO_JUGADOR
from entities.player import Player
from entities.platform import crear_plataformas_iniciales

pygame.init()
pygame.display.set_mode((1, 1))
nivel = crear_plataformas_iniciales()
jugador = Player(64, ALTO_PANTALLA - ALTURA_SUELO - ALTO_JUGADOR - 200)
teclas_vacias = pygame.key.get_pressed()

y_inicial = jugador.rect.y
for _ in range(120):
    jugador.update(teclas_vacias, nivel)
assert jugador.rect.y > y_inicial, "La gravedad no actua"
assert jugador.en_suelo is True, "No detecta el suelo"
assert jugador.rect.bottom == ALTO_PANTALLA - ALTURA_SUELO, "No queda apoyado"
assert jugador.velocidad.y == 0.0, "Velocidad vertical no se reinicia"
print("FISICA OK", jugador.rect, jugador.en_suelo)
EOF
```

Salida esperada: `FISICA OK ... True`.

**9.5 Revisión de prohibiciones**

```bash
grep -rn "time.sleep\|/home/\|C:\\\\\|password\|secret\|token" src/ || echo "SIN HALLAZGOS"
```

Debe imprimir `SIN HALLAZGOS` (o solo coincidencias justificadas y explicadas en el reporte).

**9.6 Árbol final**

```bash
find . -maxdepth 3 -not -path "./.venv/*" -not -path "./.venv" | sort
```

Debe coincidir con la sección 6.

---

## 10. Criterios de aceptación (los usará `@qa`)

- [ ] `.venv/` existe y `pygame==2.6.1` está instalado; `requirements.txt` contiene solo esa línea.
- [ ] No hay dependencias distintas de `pygame`.
- [ ] El árbol de directorios coincide exactamente con la sección 6; no hay archivos extra.
- [ ] Type hints en todas las firmas; PEP 8; docstrings en módulos, clases y métodos complejos.
- [ ] `src/config.py` centraliza pantalla, FPS, colores y física; exporta `RUTA_ASSETS` con `os.path.join`; no importa `pygame`.
- [ ] `src/main.py` contiene **solo** el Game Loop; sin constantes de física ni lógica de colisión.
- [ ] `Player` y `Platform` heredan de `pygame.sprite.Sprite`; superficies con `convert()`.
- [ ] Movimiento lateral, salto (sin doble salto), gravedad y colisión con suelo/plataformas funcionan según la sección 8.
- [ ] Cero `time.sleep()` y cero bloqueos síncronos; cadencia vía `Clock.tick(FPS)`.
- [ ] Cero credenciales codificadas en duro; cero rutas absolutas; cero escrituras fuera de las rutas autorizadas.
- [ ] `main.py` arranca headless, responde a `QUIT`/`ESC` y cierra sin excepciones.
- [ ] Las 4 verificaciones de la sección 9 se ejecutaron y su salida está en el reporte.

---

## 11. Prohibiciones explícitas (resumen)

1. Instalar cualquier paquete que no sea `pygame` (incluido `pygame-ce`).
2. Crear archivos o carpetas fuera de la sección 6.
3. Escribir código fuera de los 5 archivos de `src/` definidos (los dos `__init__.py` deben quedar vacíos).
4. Usar `time.sleep()` o cualquier espera bloqueante.
5. Usar rutas absolutas o `os.getcwd()` para localizar assets (usar `RUTA_ASSETS` de `config.py`).
6. Añadir imágenes, sonidos o fuentes externas: el sprint es 100 % primitivas de Pygame.
7. Refactorizar, "mejorar" o ampliar el alcance más allá de lo aquí descrito.
8. Incluir credenciales, tokens o datos personales en el código.

---

## 12. Entregable del `@implementador`

Al terminar, publica en el chat (no crees archivos extra) un reporte con:

1. **Estado:** `COMPLETADO` / `BLOQUEADO`.
2. **Comandos ejecutados** con su salida real (sección 9.1 a 9.6).
3. **Árbol de archivos** final.
4. **Decisiones tomadas:** solo las que esta tarea no especificaba (idealmente: ninguna).
5. **Desviaciones** respecto a este documento, si existen, con justificación.
6. **Confirmación explícita** de: sin credenciales en duro y sin operaciones de archivo fuera de las rutas autorizadas.

Luego entrega el contexto a `@qa` (sprint 01, rutas de los archivos creados y este ID de tarea) para la auditoría.
