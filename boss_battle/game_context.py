import pygame

from boss_battle.sprites_handler import SpritesHandler
from boss_battle.types_ import GameState


class GameContext:
    """Game context class."""

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        font: pygame.font.Font,
        running: bool,
        sprites_handler: SpritesHandler = SpritesHandler(),
        game_state: GameState = GameState.MAINMENU,
    ) -> None:
        self.screen = screen
        self.clock = clock
        self.font = font
        self.running = running
        self.sprites_handler = sprites_handler
        self.game_state = game_state
