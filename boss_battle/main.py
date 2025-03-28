import pygame

from boss_battle.game_context import GameContext
from boss_battle.screens.main_menu import Menu
from boss_battle.sprites.boss import Boss
from boss_battle.sprites.player import Player

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
game_context = GameContext(screen, clock, font, running=True)

player = Player(x=100, y=100, movement_speed=10, game_context=game_context)
boss = Boss(x=640, y=360, health=500, game_context=game_context)
game_context.sprites_handler.all_sprites.add(player)
game_context.sprites_handler.all_sprites.add(boss)

game_context.sprites_handler.player_sprites.add(player)
game_context.sprites_handler.boss_sprites.add(boss)

menu = Menu(game_context=game_context)

while game_context.running:
    if menu.game_state == "menu":
        menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_context.running = False
            menu.handle_input(event)
        pygame.display.flip()
        clock.tick(144)
        continue

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_context.running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game_context.running = False

        for sprite in game_context.sprites_handler.all_sprites:
            if hasattr(sprite, "handle_event"):
                sprite.handle_event(event)

    screen.fill("purple")

    game_context.sprites_handler.all_sprites.update()
    game_context.sprites_handler.all_sprites.draw(screen)

    # Process projectiles and check collisions
    collisions = pygame.sprite.groupcollide(
        game_context.sprites_handler.player_projectiles,
        game_context.sprites_handler.boss_sprites,
        True,
        False,
    )

    for sprite in collisions:
        boss.health -= 10

    # Check if boss was defeated
    if boss.health <= 0:
        menu.game_state = "menu"
        # Reset game state
        boss.health = 500
        boss.rect.x = 640
        boss.rect.y = 360
        boss.move_timer = 0

    # Render boss health
    health_text = font.render(f"Boss Health: {boss.health}", True, "white")
    screen.blit(health_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()


pygame.quit()
