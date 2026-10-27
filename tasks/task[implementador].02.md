# Tarea 02 — Corrección dirigida del Sprint 01 (cierre de brechas de la tarea 01)

- **Destinatario:** `@implementador`
- **Origen:** auditoría del `@leader` sobre `tasks/task[implementador].01.md`
- **Revisor posterior:** `@qa`
- **Estado:** cerrada — APROBADO por `@qa` (ver `tasks/sprint-01-cierre.md`)
- **Regla:** esta tarea **sustituye** a la 01 en los puntos que corrige. Todo lo no listado en la 01 sigue vigente.

---

## 0. Contexto de la auditoría

La entrega de la tarea 01 se revisó contra el contrato. El **entorno virtual sí es correcto** (`.venv` con Python 3.12.14 y `pygame==2.6.1`, único paquete instalado, `compileall` OK, sin `time.sleep`). El **código no cumple** en 9 puntos.

> Regla de honestidad: el informe anterior citó secciones ("§9", "§4/§5.3 exigía `requirements.txt`") que **no existen** en `tasks/task[implementador].01.md`. En esta entrega, cada afirmación del informe debe corresponder a una línea real del archivo o a una salida de comando pegada tal cual. Si algo no se pudo ejecutar, se escribe `NO EJECUTADO: <motivo>`.

**No recrees `.venv` ni reinstales Pygame.** Está aprobado. No toques `assets/`.

---

## 1. Defectos a corregir (lista cerrada)

### D1 — `src/config.py`: valores y nombres no coinciden con el contrato

Reescribir el módulo para que contenga **exactamente** estas constantes (mismos nombres, mismos valores, `Type Hints` y docstring de módulo):

```python
# Ventana
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_SIZE: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60
CAPTION = "Sprint 01 - Plataformas"

# Paleta
COLOR_BG = (135, 206, 235)
COLOR_GROUND = (34, 139, 34)
COLOR_PLATFORM = (139, 69, 19)
COLOR_PLAYER = (220, 20, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Física
GRAVITY = 0.8
MAX_FALL_SPEED = 18.0
PLAYER_SPEED = 5.0
JUMP_SPEED = -15.0
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 56
PLAYER_START_X = 120
PLAYER_START_Y = 300

# Nivel
GROUND_HEIGHT = 60
GROUND_TOP = SCREEN_HEIGHT - GROUND_HEIGHT
LEVEL_PLATFORMS: tuple[tuple[int, int, int, int], ...] = (
    (0, GROUND_TOP, SCREEN_WIDTH, GROUND_HEIGHT),
    (240, 400, 160, 24),
    (520, 320, 180, 24),
    (760, 240, 140, 24),
)

# Assets
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR: str = os.path.join(BASE_DIR, "assets")
IMAGES_DIR: str = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR: str = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR: str = os.path.join(ASSETS_DIR, "fonts")
```

No deben quedar alias en español (`ANCHO_PANTALLA`, `GRAVEDAD`, `RUTA_RAIZ`, etc.). **El español deja de usarse como identificador**: clases, atributos y métodos en inglés (los docstrings pueden seguir en español).

### D2 — Imports incorrectos: `python -m src.main` no arranca

- `src/main.py`, `src/entities/player.py`, `src/entities/platform.py` deben importar con rutas absolutas desde la raíz:
  - `from src.config import ...`
  - `from src.entities import Player, Platform` (o `from src.entities.player import Player`)
- `src/entities/__init__.py` debe re-exportar: `from src.entities.player import Player`, `from src.entities.platform import Platform` y definir `__all__ = ["Player", "Platform"]`.
- Prohibido manipular `sys.path`.
- Comando oficial de arranque: `.venv/bin/python -m src.main` desde la raíz. Tras la corrección, `python src/main.py` puede fallar: es aceptable y no hay que soportarlo.

### D3 — `src/main.py` no respeta el contrato del Game Loop

- **Eliminar la clase `Juego`**. `main.py` solo define `create_level() -> pygame.sprite.Group` y `main() -> None`, más el bloque `if __name__ == "__main__": main()`.
- Sin lógica de física, colisiones ni constantes propias: todo viene de `src.config`.
- `main()` debe: `pygame.init()`, `set_mode(SCREEN_SIZE)`, `set_caption(CAPTION)`, `pygame.key.set_repeat(0)`, crear `platforms = create_level()`, `player = Player(PLAYER_START_X, PLAYER_START_Y)`, `all_sprites = pygame.sprite.Group(player)` (usar `Group(player)`, no `GroupSingle`), `clock = pygame.time.Clock()`.
- Envolver el bucle en `try/finally` con `pygame.quit()` en el `finally`.
- **Falta el HUD** (defecto real): fuente creada **una sola vez** fuera del bucle con `pygame.font.SysFont("consolas", 18)`, y en cada frame dibujar en `(12, 10)`:
  - `"A/D o flechas: mover | ESPACIO: saltar | ESC: salir"`
  - `"FPS: {clock.get_fps():.0f}"`
- `clock.tick(FPS)` debe ser la **última** instrucción del frame y el único control temporal.
- Sin efectos secundarios al importar: `pygame.init()` y `set_mode()` solo dentro de `main()`.

### D4 — `Player`: colisión horizontal ausente, respawn ausente, salto repetido, API fuera de contrato

En `src/entities/player.py`:

1. Nombres de API obligatorios: `handle_input`, `apply_gravity`, `update`. Los helpers privados pueden existir, pero los tres públicos deben existir con esas firmas.
2. `update(self, platforms: pygame.sprite.Group) -> None` debe ejecutar en este orden:
   - `self.on_ground = False`
   - desplazamiento horizontal **con colisión**: mover `rect.x` y, si `pygame.sprite.spritecollide(self, platforms, False)`, revertir el desplazamiento en X y `velocity.x = 0.0`
   - clamp horizontal `0 <= rect.left` y `rect.right <= SCREEN_WIDTH`
   - salto
   - gravedad
   - desplazamiento y resolución vertical (como ya está: `rect.bottom = p.rect.top` si baja, `rect.top = p.rect.bottom` si sube)
   - **respawn**: si `rect.top > SCREEN_HEIGHT`, `rect.topleft = (PLAYER_START_X, PLAYER_START_Y)`, `velocity.update(0.0, 0.0)`
3. **Salto con flanco**: mantener `SPACE` pulsado no debe repetir saltos. Usar detección de flanco con un atributo booleano propio (`self._jump_held`) dentro de `handle_input`: solo aplica `JUMP_SPEED` cuando la tecla pasa de no pulsada a pulsada **y** `on_ground`. Está prohibido el auto-salto continuo.
4. Tamaño y arranque desde config: `PLAYER_WIDTH`, `PLAYER_HEIGHT`, `PLAYER_START_*`.
5. Renombrar atributos a inglés: `velocity`, `on_ground`.
6. Mantener `self.image.convert()` **solo** si la superficie requiere conversión tras existir el display; en este sprint es opcional. Si se conserva, documentar en el docstring que requiere `set_mode()` previo.

### D5 — `Platform`: firma y responsabilidad

- `src/entities/platform.py` debe contener **solo** la clase `Platform(pygame.sprite.Sprite)` con `__init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int] = COLOR_PLATFORM) -> None`.
  - El parámetro `color` con default **sí está permitido** (excepción aprobada por el `@leader` para poder pintar el suelo de verde).
- **Eliminar `crear_plataformas_iniciales()`**: la construcción del nivel se mueve a `create_level()` en `src/main.py`, que itera `LEVEL_PLATFORMS` y usa `COLOR_GROUND` para la primera entrada (el suelo) y `COLOR_PLATFORM` para el resto.
- Sin constantes locales de tamaño ni color duplicadas.

### D6 — Violaciones de estilo y de arquitectura pendientes

- Sin identificadores en español en clases, atributos o métodos (ver D1).
- Docstrings en todas las clases y métodos públicos.
- Imports ordenados (stdlib, terceros, locales) y sin imports sin usar.
- Líneas ≤ 99 caracteres, 4 espacios, PEP 8.

### D7 — Criterios de la tarea 01 que quedaron sin implementar

- HUD con controles y FPS (D3).
- Colisión horizontal (D4).
- Respawn al caer fuera de la pantalla (D4).
- Importabilidad (`python -m src.main`, D2).

---

## 2. Verificación obligatoria (pegar salida real)

```bash
# 1. Sintaxis
.venv/bin/python -m compileall -q src && echo COMPILE_OK

# 2. Arranque oficial headless (debe agotar el timeout, código 124)
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 5 .venv/bin/python -m src.main; echo "exit=$?"

# 3. Prohibiciones
grep -rnE "time\.sleep|pygame\.time\.(wait|delay)" src/ || echo "SIN_BLOQUEOS"
grep -rnE "from config import|from entities|import config" src/ || echo "SIN_IMPORTS_PLANOS"
grep -rnE "/home/|password|secret|token|api_key" src/ || echo "SIN_DATOS_SENSIBLES"

# 4. Prueba funcional automatizada (debe imprimir todo OK)
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python - <<'PY'
import pygame
import src.main as m
from src.config import (SCREEN_SIZE, GROUND_TOP, SCREEN_WIDTH, GROUND_HEIGHT,
                        PLAYER_START_X, PLAYER_START_Y, JUMP_SPEED)
from src.entities import Player

assert not pygame.get_init(), "main.py tiene efectos secundarios al importar"
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
platforms = m.create_level()
player = Player(PLAYER_START_X, PLAYER_START_Y)

# aterrizaje sobre el suelo
for _ in range(240):
    player.update(platforms)
assert player.on_ground and player.rect.bottom == GROUND_TOP, player.rect
print("ATERRIZAJE_OK", player.rect)

# aterrizaje sobre plataforma flotante
player.rect.topleft = (560, 200)
player.velocity.update(0, 0)
for _ in range(240):
    player.update(platforms)
assert player.on_ground and player.rect.bottom == 320, player.rect
print("PLATAFORMA_OK", player.rect)

# colisión horizontal: no atravesar el lateral de una plataforma
class Keys:
    def __init__(self, pressed=None): self.pressed = pressed or set()
    def __getitem__(self, k): return k in self.pressed

player.rect.topleft = (180, 380)          # junto al lateral izquierdo de (240, 400, 160, 24)
player.velocity.update(0, 0); player.on_ground = False
for _ in range(40):
    player.handle_input(Keys({pygame.K_RIGHT}))
    player.update(platforms)
assert player.rect.right <= 240, f"atravesó la plataforma: {player.rect}"
print("COLISION_HORIZONTAL_OK", player.rect)

# límite derecho de la pantalla
player.rect.topleft = (SCREEN_WIDTH - player.rect.width - 10, 100)
for _ in range(60):
    player.handle_input(Keys({pygame.K_RIGHT}))
    player.update(platforms)
assert player.rect.right == SCREEN_WIDTH, player.rect
print("LIMITES_OK", player.rect.right)

# salto único: mantener SPACE pulsado no debe repetir el salto en el aire
keys = Keys({pygame.K_SPACE})
player.rect.topleft = (PLAYER_START_X, GROUND_TOP - player.rect.height)
player.velocity.update(0, 0); player.on_ground = True
player.handle_input(keys)
assert player.velocity.y == JUMP_SPEED, player.velocity
for _ in range(5):
    player.handle_input(keys)        # SPACE sigue pulsado
player.update(platforms)
assert player.velocity.y > JUMP_SPEED, "auto-salto al mantener SPACE"
print("SALTO_UNICO_OK", player.velocity.y)

# respawn al caer fuera de la pantalla
player.rect.topleft = (0, SCREEN_SIZE[1] + 50)
player.update(platforms)
assert player.rect.topleft == (PLAYER_START_X, PLAYER_START_Y), player.rect
print("RESPAWN_OK", player.rect)
pygame.quit()
print("TODO OK")
PY

# 5. Árbol final sin archivos extra
find src assets -type f -not -path "*/__pycache__/*" | sort
```

Además, comprobación visual de 10 s con display real:

```bash
timeout 10 .venv/bin/python -m src.main; echo "exit=$?"
```

- [ ] Ventana de **960x540** con título `Sprint 01 - Plataformas`.
- [ ] HUD visible arriba a la izquierda con controles y FPS.
- [ ] El jugador (rectángulo rojo 40x56) se mueve, salta una sola vez por pulsación, cae y aterriza sobre el suelo verde y las 3 plataformas marrones.
- [ ] El jugador no atraviesa lateralmente las plataformas.
- [ ] `ESC` y la `X` cierran sin traceback.

---

## 3. Criterios de aceptación para `@qa`

1. `tasks/task[implementador].02.md` completado en todos los puntos D1–D7.
2. Los 5 bloques de la sección 2 ejecutados con salida pegada; `TODO OK` presente en el bloque 4.
3. `src/config.py` contiene exactamente las constantes del punto D1 (verificable con `grep` de `SCREEN_WIDTH = 960` y `GROUND_TOP`).
4. `src/main.py` no define clases y sí define `create_level` y `main`.
5. Cero identificadores en español en el código (revisar `ANCHO_`, `ALTO_`, `GRAVEDAD`, `TITULO_`, `RUTA_`, `_mover_`, `_aplicar`, `en_suelo`, `velocidad`, `teclas`, `plataformas`, `pantalla`, `reloj`, `ejecutando`).
6. Sin `time.sleep`, sin `sys.path`, sin `eval`/`exec`, sin borrados de archivos, sin rutas absolutas.
7. Solo `pygame==2.6.1` y `pip` en `.venv`.

---

## 4. Formato del informe de cierre

1. Tabla `D1..D7 → estado (corregido / no aplica) → archivo y línea`.
2. Salida literal de los 5 comandos de la sección 2.
3. `diff` resumido por archivo (`git diff --no-index` no está disponible; basta indicar qué cambió en cada archivo).
4. Desviaciones nuevas (si las hay) **con justificación y sin reinterpretar el contrato**.
5. Confirmación de rutas no tocadas.

Al terminar, actualizar la cabecera de **este** archivo a `Estado: implementada (pendiente de QA)` y la de `tasks/task[implementador].01.md` a `Estado: implementada (ver tarea 02)`.
