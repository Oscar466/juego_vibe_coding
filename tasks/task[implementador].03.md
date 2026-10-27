# Tarea 03 — Cierre de jugabilidad del Sprint 01 (muro invisible y holgura del nivel)

- **Destinatario:** `@implementador`
- **Origen:** revisión del `@leader` sobre la entrega de la tarea 02
- **Revisor posterior:** `@qa`
- **Estado:** cerrada — APROBADO por `@qa` (ver `tasks/sprint-01-cierre.md`)
- **Alcance:** 2 correcciones puntuales. **No** refactorizar nada más. Todo lo demás de las tareas 01 y 02 sigue vigente.

---

## 0. Diagnóstico

La entrega de la tarea 02 compila, arranca en 960x540, muestra el HUD y pasa el test del contrato. Pero el `@leader` detectó que la solución de colisión horizontal **rompe el juego**:

- `src/entities/player.py:78-89` amplía la sonda de colisión **1 px hacia arriba**.
- Con `LEVEL_PLATFORMS[1] = (240, 400, 160, 24)`, la cara inferior de esa plataforma está en `y = 424` y el jugador de pie sobre el suelo tiene `top = 424`.
- Por tanto la sonda entra en la plataforma y el jugador **queda bloqueado en `x = 200`**, sin poder avanzar por el suelo más allá de 80 px del inicio. Es un muro invisible.
- El propio test de la tarea 02 "avalaba" ese comportamiento (`COLISION_HORIZONTAL_OK <rect(200, 424, 40, 56)>`), pero el test estaba mal planteado: comprobaba bloqueo donde la geometría del nivel simplemente no debía bloquear. **El defecto es del contrato, no tuyo**; se corrige aquí.

Causa raíz doble: (a) la sonda de 1 px es innecesaria, porque `colliderect` solo considera solapamiento real y el jugador pasa justo por debajo; (b) la holgura entre suelo y plataformas es de 0 px (56 px de hueco para un jugador de 56 px), lo que hace el paso agobiante.

---

## 1. Correcciones

### F1 — Eliminar la sonda de 1 px y usar colisión horizontal estándar

En `src/entities/player.py`, el bloque de desplazamiento horizontal dentro de `update` debe quedar así (sin `probe`, sin `probe.top -= 1`):

```python
dx: int = int(round(self.velocity.x))
if dx != 0:
    self.rect.x += dx
    if pygame.sprite.spritecollide(self, platforms, False):
        self.rect.x -= dx
        self.velocity.x = 0.0
```

- Mantener el clamp `0 <= rect.left` y `rect.right <= SCREEN_WIDTH`.
- Eliminar el comentario justificativo de la sonda.
- No cambiar el orden del resto de `update` (gravedad, movimiento vertical, resolución vertical, respawn).

### F2 — Subir las plataformas flotantes para dar holgura (cambio autorizado)

Sustituir en `src/config.py` el valor de `LEVEL_PLATFORMS` por (esto **modifica** el bloque D1 de la tarea 02; es una revisión aprobada por el `@leader`):

```python
LEVEL_PLATFORMS: tuple[tuple[int, int, int, int], ...] = (
    (0, GROUND_TOP, SCREEN_WIDTH, GROUND_HEIGHT),
    (240, 380, 160, 24),
    (520, 300, 180, 24),
    (760, 220, 140, 24),
)
```

Comprobación de diseño que debes respetar (no la alteres):
- Holgura bajo la primera plataforma: `480 - (380 + 24) = 76 px` > 56 px del jugador → se pasa caminando.
- Altura de salto disponible: `JUMP_SPEED² / (2·GRAVITY) = 225 / 1.6 ≈ 140 px`, suficiente para subir de 480→380, 380→300 y 300→220.

---

## 2. Verificación obligatoria (pegar salida literal; sustituye al bloque 4 de la tarea 02)

```bash
.venv/bin/python -m compileall -q src && echo COMPILE_OK

SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 5 .venv/bin/python -m src.main; echo "exit=$?"

grep -rnE "probe" src/ || echo "SIN_SONDA"
grep -rnE "time\.sleep|pygame\.time\.(wait|delay)|sys\.path|eval\(|exec\(|os\.remove|shutil" src/ || echo SIN_PROHIBIDOS

SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python - <<'PY'
import pygame
import src.main as m
from src.config import (SCREEN_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_TOP,
                        PLAYER_HEIGHT, PLAYER_START_X, PLAYER_START_Y,
                        JUMP_SPEED, GRAVITY)
from src.entities import Player

assert not pygame.get_init(), "main.py tiene efectos secundarios al importar"
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
platforms = m.create_level()
player = Player(PLAYER_START_X, PLAYER_START_Y)

class Keys:
    def __init__(self, pressed=None): self.pressed = pressed or set()
    def __getitem__(self, k): return k in self.pressed

def step(keys, frames=1):
    for _ in range(frames):
        player.handle_input(keys)
        player.update(platforms)

# 1. Caída y aterrizaje sobre el suelo
step(Keys(), 240)
assert player.on_ground and player.rect.bottom == GROUND_TOP, player.rect
print("ATERRIZAJE_OK", player.rect)

# 2. REGRESIÓN CLAVE: se puede caminar por el suelo bajo las 3 plataformas
player.rect.topleft = (PLAYER_START_X, GROUND_TOP - PLAYER_HEIGHT)
player.velocity.update(0, 0); player.on_ground = True
pasos = 0
while player.rect.right < SCREEN_WIDTH and pasos < 400:
    step(Keys({pygame.K_RIGHT}), 1); pasos += 1
assert player.rect.right == SCREEN_WIDTH, f"muro invisible en {player.rect}"
print("SIN_MURO_INVISIBLE_OK", pasos, "frames", player.rect)

# 3. Colisión lateral real contra una plataforma a la altura del torso
player.rect.topleft = (480, 300)          # plataforma (520, 300, 180, 24)
player.velocity.update(0, 0)
step(Keys({pygame.K_RIGHT}), 1)
assert player.rect.right == 520, f"atravesó la plataforma: {player.rect}"
print("COLISION_LATERAL_OK", player.rect)

# 4. Aterrizaje sobre la primera plataforma flotante (top = 380)
player.rect.topleft = (300, 100)
player.velocity.update(0, 0)
step(Keys(), 240)
assert player.on_ground and player.rect.bottom == 380, player.rect
print("PLATAFORMA_OK", player.rect)

# 5. Salto único (mantener SPACE no repite el salto)
#    Enmienda A1: el impulso se comprueba justo tras handle_input, antes de
#    que update aplique la gravedad de ese mismo frame.
player.rect.topleft = (PLAYER_START_X, GROUND_TOP - PLAYER_HEIGHT)
player.velocity.update(0, 0); player.on_ground = True
player.handle_input(Keys({pygame.K_SPACE}))
assert player.velocity.y == JUMP_SPEED, player.velocity
for _ in range(5):
    player.handle_input(Keys({pygame.K_SPACE}))
    player.update(platforms)
assert not player.on_ground, "el jugador no despegó"
assert player.velocity.y > JUMP_SPEED + 4 * GRAVITY, "auto-salto al mantener SPACE"
print("SALTO_UNICO_OK", player.velocity.y)

# 6. Respawn al caer fuera de la pantalla
player.rect.topleft = (0, SCREEN_HEIGHT + 60)
player.velocity.update(0, 0)
step(Keys(), 1)
assert player.rect.topleft == (PLAYER_START_X, PLAYER_START_Y), player.rect
print("RESPAWN_OK", player.rect)

pygame.quit()
print("TODO OK")
PY
```

Comprobación visual (10 s con display real):

```bash
timeout 10 .venv/bin/python -m src.main; echo "exit=$?"
```

- [ ] Avanzar con `D` desde el inicio **recorre toda la pantalla** sin detenerse en `x = 200`.
- [ ] Las 3 plataformas flotantes quedan por encima de la cabeza del jugador.
- [ ] Se puede saltar sobre la primera plataforma (380), la segunda (300) y la tercera (220).
- [ ] Se puede saltar y caminar por el suelo sin quedar enganchado en ningún borde.

---

## 3. Criterios de aceptación para `@qa`

1. `grep -rn "probe" src/` → sin resultados.
2. `LEVEL_PLATFORMS` en `src/config.py` contiene `(240, 380, 160, 24)`, `(520, 300, 180, 24)` y `(760, 220, 140, 24)`.
3. La secuencia de la sección 2 imprime `SIN_MURO_INVISIBLE_OK` seguido de `TODO OK`.
4. `python -m src.main` arranca en 960x540 con HUD y cierra limpio.
5. No hay cambios en archivos fuera de `src/config.py` y `src/entities/player.py` (más las cabeceras de estado de `tasks/`).
6. Siguen vigentes los criterios 3–7 de la tarea 02.

---

## 4. Informe de cierre

1. Tabla `F1/F2 → estado → archivo y líneas`.
2. Salida literal de los 4 bloques de la sección 2.
3. Confirmación de que solo se tocaron `src/config.py` y `src/entities/player.py`.
4. Desviaciones (si las hay), sin reinterpretar el contrato.

Al terminar: `Estado: implementada (pendiente de QA)` en este archivo.

---

## 5. Enmienda A1 — aprobada por el `@leader` (2026-10-27)

**Diagnóstico aceptado:** el assert 5 del bloque 4 de la sección 2 era defectuoso. Medía `velocity.y` después de un `step()` completo (input + gravedad), por lo que esperar `JUMP_SPEED` exacto era imposible: el valor correcto tras un frame es `JUMP_SPEED + GRAVITY`. El `@implementador` acertó al no parchear el código para satisfacer un test mal escrito.

**Cambio autorizado (ya aplicado en el bloque 4 de arriba):**

1. El assert inmediato de `JUMP_SPEED` se evalúa justo después de `handle_input`, antes del `update()` de ese frame.
2. Se añade `assert not player.on_ground` para confirmar el despegue.
3. La condición anti-auto-salto pasa a ser `velocity.y > JUMP_SPEED + 4 * GRAVITY` (con 5 frames de gravedad acumulada, el valor real es ≈ -10.2; si el salto se repitiera cada frame quedaría en ≈ -14.2 y el test fallaría).
4. Se importa `GRAVITY` en el script.

**No cambia nada del código de `src/`**: F1 y F2 siguen tal como están implementados. Solo se corrige el contrato de verificación.

**Tareas de cierre para el `@implementador`:**

1. Ejecutar el bloque 4 enmendado y pegar la salida completa, que debe terminar en `TODO OK`.
2. Limpiar los artefactos de bytecode: `find src -name __pycache__ -type d -prune -exec rm -rf {} +` (permitido: solo dentro de `src/`).
3. Reportar el resultado final en 5 líneas.

Con esto, el criterio de aceptación 3 de la sección 3 se lee como: el bloque 4 enmendado imprime `SIN_MURO_INVISIBLE_OK`, `COLISION_LATERAL_OK`, `PLATAFORMA_OK`, `SALTO_UNICO_OK`, `RESPAWN_OK` y `TODO OK`.
