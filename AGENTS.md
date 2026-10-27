# Contexto Global del Proyecto: Juego en Pygame

## 1. Stack Técnico y Arquitectura
- **Lenguaje principal:** Python 3.10+ (Es obligatorio el uso de *Type Hints* en todo el código).
- **Librería principal:** Pygame (Manejo de gráficos, eventos, colisiones y sonidos).
- **Arquitectura exigida:** Programación Orientada a Objetos (OOP) con separación estricta de responsabilidades.
  - `src/main.py`: Solo debe contener el *Game Loop* principal (inicialización, captura de eventos, actualización y dibujado).
  - `src/entities/`: Todas las entidades (Jugador, Enemigos, Obstáculos) deben heredar de `pygame.sprite.Sprite`.
  - `src/config.py`: Archivo único para centralizar variables globales (tamaño de pantalla, FPS, paleta de colores).
  

## 2. Reglas de Oro y Seguridad
- **Permisos estrictos:** Ningún agente puede modificar archivos fuera de la carpeta autorizada (`src/` y `specs/`) sin permiso explícito (`ask_user`).
- **Dependencias controladas:** Prohibido inventar o instalar librerías externas adicionales mediante `pip` que no sean Pygame, a menos que el humano lo autorice.
- **Manejo de Assets:** Todas las imágenes, fuentes y sonidos deben guardarse en la carpeta `assets/` y cargarse usando rutas relativas dinámicas (`os.path.join`), nunca rutas absolutas.
- **Entorno:** Las dependencias deben ser instaladas en un ambiente `.venv`  

## 3. Estándares de Código
- Cumplimiento estricto de la convención de estilo **PEP 8**.
- Optimización: Las imágenes deben cargarse usando `convert()` o `convert_alpha()` para no saturar la memoria y evitar caídas de FPS.
- Comentarios: Cada clase y método complejo debe estar documentado para que el resto de agentes entienda el flujo.

## 4. Modo de trabajo
- La forma en que se trabajará será por sprints de desarrollo, cada archivo de la carpeta `specs/` será una etapa del desarrollo, se enumerarán de 1 a n.

## 5. Orquestación (Flujo del Harness)
- **@leader:** Coordina el proyecto leyendo secuencialmente los archivos en `specs/`. Nunca programa directamente.
- **@implementador:** Escribe la lógica modularizada según la directriz del líder.
- **@qa:** Audita el código generado para asegurar que el *Game Loop* nunca se bloquee de forma síncrona (por ejemplo, prohibido usar `time.sleep()`).