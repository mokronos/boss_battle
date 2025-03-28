import math

import pygame

from boss_battle.game_context import GameContext
from boss_battle.sprites.stats import Stats


class Boss(pygame.sprite.Sprite):
    """Boss class."""

    def __init__(self, x: int, y: int, stats: Stats, game_context: GameContext) -> None:
        """Boss constructor."""
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.stats = stats
        self.move_timer = 0  # For movement pattern
        self.game_context = game_context

    def update(self, *args: tuple, **kwargs: tuple) -> None:
        """Update boss position with smooth movement pattern."""
        super().update(*args, **kwargs)
        self.move_timer += 0.02
        self.rect.x += int(math.cos(self.move_timer) * 1.5)  # Horizontal wave pattern
        self.rect.y += int(
            math.sin(self.move_timer * 0.8) * 1.2
        )  # Vertical wave pattern
