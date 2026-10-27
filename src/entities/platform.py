"""Plataformas estáticas: el suelo y las plataformas flotantes del nivel."""

import pygame

from src.config import COLOR_PLATFORM


class Platform(pygame.sprite.Sprite):
    """Cuerpo estático (suelo o plataforma flotante).

    Representa tanto el suelo del nivel como las plataformas sobre las que el
    jugador puede apoyarse. Es un rectángulo sólido sin animación ni
    desplazamiento. La superficie se convierte con ``convert()``, por lo que
    debe existir un display (``pygame.display.set_mode()``) antes de crear la
    plataforma.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: tuple[int, int, int] = COLOR_PLATFORM,
    ) -> None:
        """Crea la superficie coloreada y ubica su rect en ``(x, y)``."""
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((width, height))
        self.image.fill(color)
        self.image = self.image.convert()
        self.rect: pygame.Rect = self.image.get_rect(topleft=(x, y))
