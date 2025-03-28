import pygame

from boss_battle.game_context import GameContext
from boss_battle.handle_collission import handle_collisions
from boss_battle.screens.main_menu import MainMenu
from boss_battle.sprites.boss import Boss
from boss_battle.sprites.player import Player
from boss_battle.sprites.stats import Stats
from boss_battle.types_ import GameState

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_context = GameContext(screen, clock, font, running=True)

player = Player(
    x=100,
    y=100,
    game_context=game_context,
    stats=Stats(health=100, damage=10, attack_speed=10, movement_speed=5),
)
boss = Boss(
    x=640,
    y=360,
    game_context=game_context,
    stats=Stats(health=500, damage=20, attack_speed=1, movement_speed=2),
)
game_context.sprites_handler.all_sprites.add(player)
game_context.sprites_handler.all_sprites.add(boss)

game_context.sprites_handler.player_sprites.add(player)
game_context.sprites_handler.boss_sprites.add(boss)

menu = MainMenu(game_context=game_context)

while game_context.running:
    delta_time = clock.tick(144) / 1000  # Time elapsed in seconds since the last frame

    match game_context.game_state:
        case GameState.MAINMENU:
            menu.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_context.running = False
                menu.handle_input(event)

        case GameState.PLAYING:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_context.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                    game_context.running = False

            screen.fill("purple")

            for sprite in game_context.sprites_handler.all_sprites:
                if hasattr(sprite, "handle_events"):
                    sprite.handle_events()

            game_context.sprites_handler.all_sprites.update(delta_time)
            game_context.sprites_handler.all_sprites.draw(game_context.screen)
            handle_collisions(game_context)

            # Render boss health
            health_text = font.render(
                f"Boss Health: {boss.stats.health}", True, "white"
            )
            screen.blit(health_text, (10, 10))

            # Render player health
            player_health_text = font.render(
                f"Player Health: {player.stats.health}", True, "white"
            )
            screen.blit(player_health_text, (10, 40))
        case _:
            raise ValueError(f"Unknown game state: {game_context.game_state}")

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()
