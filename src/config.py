"""Constantes globales del juego (ventana, paleta, física y nivel).

Este módulo es el único punto de verdad para los valores configurables del
proyecto. No debe importar ``pygame`` ni contener lógica de juego.
"""

import os

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
    (240, 380, 160, 24),
    (520, 300, 180, 24),
    (760, 220, 140, 24),
)

# Assets
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR: str = os.path.join(BASE_DIR, "assets")
IMAGES_DIR: str = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR: str = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR: str = os.path.join(ASSETS_DIR, "fonts")
