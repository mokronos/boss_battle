import math

import pygame

from boss_battle.game_context import GameContext


class Boss(pygame.sprite.Sprite):
    """Boss class."""

    def __init__(self, x: int, y: int, health: int, game_context: GameContext) -> None:
        """Boss constructor."""
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.max_health = health  # Track max health for health bar
        self.move_timer = 0  # For movement pattern
        self.game_context = game_context

    # def draw(self) -> None:
    #     """Draw boss with core, outline, and health bar."""
    #     # Yellow outline
    #     pygame.draw.circle(screen, "yellow", (self.rect.x, self.rect.y), 45, 5)
    #     # Green core
    #     pygame.draw.circle(screen, "darkgreen", (self.rect.x, self.rect.y), 40)

    #     # Health bar
    #     health_width = 100
    #     current_health_width = (self.health / self.max_health) * health_width
    #     pygame.draw.rect(screen, "red", (self.rect.x - 50, self.rect.y - 70, health_width, 10))
    #     pygame.draw.rect(
    #         screen, "green", (self.rect.x - 50, self.rect.y - 70, current_health_width, 10)
    #     )

    def update(self) -> None:
        """Update boss position with smooth movement pattern."""
        self.move_timer += 0.02
        self.rect.x += int(math.cos(self.move_timer) * 1.5)  # Horizontal wave pattern
        self.rect.y += int(
            math.sin(self.move_timer * 0.8) * 1.2
        )  # Vertical wave pattern
