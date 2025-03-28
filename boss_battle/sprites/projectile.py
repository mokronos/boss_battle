import pygame

from boss_battle.game_context import GameContext


class Projectile(pygame.sprite.Sprite):
    """Projectile class."""

    def __init__(
        self,
        x: int,
        y: int,
        velocity: tuple[int, int],
        damage: int,
        game_context: GameContext,
    ) -> None:
        """Projectile constructor."""
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.damage = damage
        self.game_context = game_context

    def update(self, *args: tuple, **kwargs: tuple) -> None:
        """Update projectile."""
        super().update(*args, **kwargs)
        self.rect.x += self.velocity[0] * 10
        self.rect.y += self.velocity[1] * 10

    def move(self, x: int, y: int) -> None:
        """Move projectile."""
        self.rect.x += x
        self.rect.y += y
