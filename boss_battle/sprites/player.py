import pygame
from boss_battle.sprites.projectile import Projectile


class Player(pygame.sprite.Sprite):
    """Player class."""

    def __init__(self, x: int, y: int, movement_speed: int) -> None:
        """Player constructor."""
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill("blue")
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.velocity: tuple[int, int] = (0, 0)
        self.movement_speed = movement_speed

    def draw(self) -> None:
        """Draw player."""
        pass

    def update(self) -> None:
        """Update player position."""
        self.rect.x += self.velocity[0] * self.movement_speed
        self.rect.y += self.velocity[1] * self.movement_speed

    def handle_event(self, event: pygame.event.Event) -> None:
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
        if not keys[pygame.K_x] and not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity = (0, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            len_vec = ((x_mouse - self.rect.x) ** 2 + (y_mouse - self.rect.y) ** 2) ** 0.5
            vel = ((x_mouse - self.rect.x) / len_vec, (y_mouse - self.rect.y) / len_vec)
            projectile = Projectile(self.rect.x, self.rect.y, velocity=vel)
            all_sprites.add(projectile)
            player_projectiles.add(projectile)
