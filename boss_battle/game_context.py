import pygame

from boss_battle.sprites_handler import SpritesHandler


class GameContext:
    """Game context class."""

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        font: pygame.font.Font,
        running: bool,
        sprites_handler: SpritesHandler = SpritesHandler(),
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.font = font
        self.running = running
        self.sprites_handler = sprites_handler
