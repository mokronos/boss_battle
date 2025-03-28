import pygame
from boss_battle.sprites.boss import Boss
from boss_battle.sprites.player import Player
from boss_battle.sprites.projectile import Projectile
from boss_battle.screens.main_menu import Menu


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True
dt = 0

all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
boss_sprites = pygame.sprite.Group()
player_projectiles = pygame.sprite.Group()

player = Player(x=100, y=100, movement_speed=10)
boss = Boss(x=640, y=360, health=500)
all_sprites.add(player)
all_sprites.add(boss)

player_sprites.add(player)
boss_sprites.add(boss)

menu = Menu()

while running:
    if menu.game_state == "menu":
        menu.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            menu.handle_input(event)
        pygame.display.flip()
        clock.tick(144)
        continue

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            running = False

        for sprite in all_sprites:
            if hasattr(sprite, "handle_event"):
                sprite.handle_event(event)

    screen.fill("purple")

    all_sprites.update()
    all_sprites.draw(screen)

    # Process projectiles and check collisions
    collisions = pygame.sprite.groupcollide(player_projectiles, boss_sprites, True, False)
    print(collisions)

    for sprite in collisions:
        print("hello")
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

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(144) / 1000

pygame.quit()
