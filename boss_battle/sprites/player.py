import pygame

from boss_battle.game_context import GameContext
from boss_battle.sprites.projectile import Projectile
from boss_battle.sprites.stats import Stats


class Player(pygame.sprite.Sprite):
    """Player class."""

    def __init__(self, x: int, y: int, stats: Stats, game_context: GameContext) -> None:
        """Player constructor."""
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill("blue")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.velocity: tuple[int, int] = (0, 0)
        self.stats = stats
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

        # Calculate projectile direction toward mouse position
        x_mouse, y_mouse = pygame.mouse.get_pos()
        len_vec = (
            (x_mouse - self.rect.centerx) ** 2 + (y_mouse - self.rect.centery) ** 2
        ) ** 0.5

        # Avoid division by zero
        if len_vec == 0:
            return

        vel = (
            (x_mouse - self.rect.centerx) / len_vec,
            (y_mouse - self.rect.centery) / len_vec,
        )

        # Create projectile at player's center
        projectile = Projectile(
            self.rect.centerx,
            self.rect.centery,
            velocity=vel,
            game_context=self.game_context,
            damage=self.stats.damage,
        )

        # Add projectile to sprite groups
        self.game_context.sprites_handler.all_sprites.add(projectile)
        self.game_context.sprites_handler.player_projectiles.add(projectile)

    def draw(self) -> None:
        """Draw player."""
        pass

    def update(self, *args: tuple, **kwargs: tuple) -> None:
        """Update player position."""
        super().update(*args, **kwargs)
        x_new = self.rect.x + self.velocity[0] * self.stats.movement_speed
        y_new = self.rect.y + self.velocity[1] * self.stats.movement_speed

        if (
            x_new >= 0
            and x_new <= self.game_context.screen.get_width() - self.rect.width
        ):
            self.rect.x = x_new
        if (
            y_new >= 0
            and y_new <= self.game_context.screen.get_height() - self.rect.height
        ):
            self.rect.y = y_new

    def handle_events(self) -> None:
        """Handle user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.velocity = (self.velocity[0], -1)
        if keys[pygame.K_s]:
            self.velocity = (self.velocity[0], 1)
        if keys[pygame.K_a]:
            self.velocity = (-1, self.velocity[1])
        if keys[pygame.K_d]:
            self.velocity = (1, self.velocity[1])
        if (
            not keys[pygame.K_w]
            and not keys[pygame.K_s]
            and not keys[pygame.K_a]
            and not keys[pygame.K_d]
        ):
            self.velocity = (0, 0)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.attack()
