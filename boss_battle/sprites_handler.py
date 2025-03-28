import pygame


class SpritesHandler:
    """Handles all the sprites."""

    def __init__(self) -> None:
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.boss_sprites = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
