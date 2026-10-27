"""Jugador controlable: movimiento lateral, salto, gravedad y colisiones."""

import pygame

from src.config import (
    COLOR_PLAYER,
    GRAVITY,
    JUMP_SPEED,
    MAX_FALL_SPEED,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Player(pygame.sprite.Sprite):
    """Jugador controlable con física de plataformas.

    La superficie se construye con ``pygame.Surface`` y se convierte con
    ``convert()``; por tanto, debe existir un display (``set_mode()``) antes
    de instanciar la clase.
    """

    def __init__(self, x: int, y: int) -> None:
        """Crea la superficie del jugador y su estado físico inicial."""
        super().__init__()
        self.image: pygame.Surface = pygame.Surface(
            (PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self.image.fill(COLOR_PLAYER)
        self.image = self.image.convert()
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0.0, 0.0)
        self.on_ground: bool = False
        self._jump_held: bool = False

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Traduce las teclas en velocidad horizontal y salto con flanco.

        El salto solo se aplica cuando la tecla de salto pasa de no pulsada a
        pulsada (flanco) y el jugador está en el suelo; mantener SPACE pulsado
        no repite el salto.
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = PLAYER_SPEED
        else:
            self.velocity.x = 0.0

        jump_pressed: bool = bool(
            keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        )
        if jump_pressed and not self._jump_held and self.on_ground:
            self.velocity.y = JUMP_SPEED
            self.on_ground = False
        self._jump_held = jump_pressed

    def apply_gravity(self) -> None:
        """Incrementa la velocidad de caída hasta el límite permitido."""
        self.velocity.y = min(self.velocity.y + GRAVITY, MAX_FALL_SPEED)

    def update(self, platforms: pygame.sprite.Group) -> None:
        """Avanza un frame de simulación del jugador.

        El orden es determinista: reinicio de ``on_ground``, desplazamiento
        horizontal con colisión, límites de pantalla, salto, gravedad,
        desplazamiento y resolución vertical, y respawn si cae de la pantalla.
        El impulso de salto se aplica en ``handle_input`` (detección de flanco)
        para no repetir el salto al mantener la tecla pulsada.
        """
        self.on_ground = False

        dx: int = int(round(self.velocity.x))
        if dx != 0:
            self.rect.x += dx
            if pygame.sprite.spritecollide(self, platforms, False):
                self.rect.x -= dx
                self.velocity.x = 0.0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.apply_gravity()

        self.rect.y += int(round(self.velocity.y))
        for platform in pygame.sprite.spritecollide(self, platforms, False):
            if self.velocity.y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0.0
                self.on_ground = True
            elif self.velocity.y < 0:
                self.rect.top = platform.rect.bottom
                self.velocity.y = 0.0

        if self.rect.top > SCREEN_HEIGHT:
            self.rect.topleft = (PLAYER_START_X, PLAYER_START_Y)
            self.velocity.update(0.0, 0.0)
