"""Game Loop principal del Sprint 01: inicialización, eventos, update y draw."""

import pygame

from src.config import (
    CAPTION,
    COLOR_BG,
    COLOR_GROUND,
    COLOR_PLATFORM,
    COLOR_TEXT,
    FPS,
    LEVEL_PLATFORMS,
    PLAYER_START_X,
    PLAYER_START_Y,
    SCREEN_SIZE,
)
from src.entities import Player, Platform


def create_level() -> pygame.sprite.Group:
    """Construye el nivel: el suelo en verde y el resto en marrón.

    La primera entrada de ``LEVEL_PLATFORMS`` es el suelo (se pinta con
    ``COLOR_GROUND``) y las siguientes son plataformas flotantes.
    """
    platforms: pygame.sprite.Group = pygame.sprite.Group()
    for index, (x, y, width, height) in enumerate(LEVEL_PLATFORMS):
        color: tuple[int, int, int] = (
            COLOR_GROUND if index == 0 else COLOR_PLATFORM
        )
        platforms.add(Platform(x, y, width, height, color))
    return platforms


def main() -> None:
    """Punto de entrada: inicializa Pygame y ejecuta el bucle principal."""
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(CAPTION)
    pygame.key.set_repeat(0)

    platforms: pygame.sprite.Group = create_level()
    player: Player = Player(PLAYER_START_X, PLAYER_START_Y)
    all_sprites: pygame.sprite.Group = pygame.sprite.Group(player)
    clock: pygame.time.Clock = pygame.time.Clock()
    font: pygame.font.Font = pygame.font.SysFont("consolas", 18)

    running: bool = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE
                ):
                    running = False
            if not running:
                break

            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            player.handle_input(keys)
            player.update(platforms)

            screen.fill(COLOR_BG)
            platforms.draw(screen)
            all_sprites.draw(screen)
            controls: pygame.Surface = font.render(
                "A/D o flechas: mover | ESPACIO: saltar | ESC: salir",
                True,
                COLOR_TEXT,
            )
            screen.blit(controls, (12, 10))
            fps_text: pygame.Surface = font.render(
                f"FPS: {clock.get_fps():.0f}",
                True,
                COLOR_TEXT,
            )
            screen.blit(fps_text, (12, 34))
            pygame.display.flip()

            clock.tick(FPS)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
