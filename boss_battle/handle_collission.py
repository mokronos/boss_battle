import pygame

from boss_battle.game_context import GameContext
from boss_battle.types_ import GameState


def handle_collisions(game_context: GameContext) -> None:
    """Handle collisions between characers and projectiles."""
    for player in game_context.sprites_handler.player_sprites:
        collisions = pygame.sprite.spritecollide(
            player,
            game_context.sprites_handler.boss_projectiles,
            True,
        )
        for sprite in collisions:
            if not hasattr(sprite, "damage"):
                raise Exception("Collided sprite does not have damage attribute")
            player.stats.health -= sprite.damage

        if player.stats.health <= 0:
            game_context.game_state = GameState.MAINMENU
            # Reset game state
            player.stats.health = 100
            player.rect.x = 100
            player.rect.y = 100
            player.move_timer = 0

    for boss in game_context.sprites_handler.boss_sprites:
        collisions = pygame.sprite.spritecollide(
            boss,
            game_context.sprites_handler.player_projectiles,
            True,
        )

        for sprite in collisions:
            if not hasattr(sprite, "damage"):
                raise Exception("Collided sprite does not have damage attribute")
            boss.stats.health -= sprite.damage

        if boss.stats.health <= 0:
            game_context.game_state = GameState.MAINMENU
            # Reset game state
            boss.stats.health = 500
            boss.rect.x = 640
            boss.rect.y = 360
            boss.move_timer = 0
