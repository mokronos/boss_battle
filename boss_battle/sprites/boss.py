import math

import pygame

from boss_battle.game_context import GameContext
from boss_battle.sprites.projectile import Projectile
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

        self.last_attack_time = 0

    def can_attack(self) -> bool:
        """Check if enough time has passed to allow another attack."""
        current_time = pygame.time.get_ticks()
        # Convert attack speed to milliseconds between attacks
        attack_cooldown = 1000 / self.stats.attack_speed
        return current_time - self.last_attack_time >= attack_cooldown

    def attack(self) -> None:
        """Create a projectile if attack cooldown has passed."""
        if not self.can_attack():
            return

        # Update the last attack time to current time
        self.last_attack_time = pygame.time.get_ticks()

        num_projectiles = 20
        speed_projectiles = 5
        center = self.rect.center

        for i in range(num_projectiles):
            angle_rad = math.radians((360 / num_projectiles) * i)
            vx = math.cos(angle_rad)
            vy = math.sin(angle_rad)
            proj = Projectile(
                x=center[0],
                y=center[1],
                velocity=(vx, vy),
                speed=speed_projectiles,
                damage=self.stats.damage,
                game_context=self.game_context,
            )
            self.game_context.sprites_handler.boss_projectiles.add(proj)
            self.game_context.sprites_handler.all_sprites.add(proj)


    def update(self, *args: tuple, **kwargs: tuple) -> None:
        """Update boss position with smooth movement pattern."""
        super().update(*args, **kwargs)
        self.move_timer += 0.02
        self.rect.x += int(math.cos(self.move_timer) * 1.5)  # Horizontal wave pattern
        self.rect.y += int(
            math.sin(self.move_timer * 0.8) * 1.2
        )  # Vertical wave pattern

        self.attack()
