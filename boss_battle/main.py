import math

import pygame


class Menu:
    """Main menu with start and quit buttons."""

    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.game_state = "menu"

    def draw(self, screen: pygame.Surface) -> None:
        """Draw menu with start and quit buttons."""
        screen.fill("purple")
        # Title
        text = self.font.render("BOSS BATTLE", True, "white")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 100))

        # Start button
        self.start_rect = pygame.Rect(1280 // 2 - 100, 300, 200, 50)
        pygame.draw.rect(screen, "green", self.start_rect)
        text = self.small_font.render("START", True, "white")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 310))

        # Quit button
        self.quit_rect = pygame.Rect(1280 // 2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, "red", self.quit_rect)
        text = self.small_font.render("QUIT", True, "white")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 410))

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle user input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                self.game_state = "playing"
            elif self.quit_rect.collidepoint(event.pos):
                pygame.quit()
                raise SystemExit


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
running = True
dt = 0


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

class Boss(pygame.sprite.Sprite):
    """Boss class."""

    def __init__(self, x: int, y: int, health: int) -> None:
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

    def draw(self) -> None:
        """Draw boss with core, outline, and health bar."""
        # Yellow outline
        pygame.draw.circle(screen, "yellow", (self.rect.x, self.rect.y), 45, 5)
        # Green core
        pygame.draw.circle(screen, "darkgreen", (self.rect.x, self.rect.y), 40)

        # Health bar
        health_width = 100
        current_health_width = (self.health / self.max_health) * health_width
        pygame.draw.rect(screen, "red", (self.rect.x - 50, self.rect.y - 70, health_width, 10))
        pygame.draw.rect(
            screen, "green", (self.rect.x - 50, self.rect.y - 70, current_health_width, 10)
        )

    def update(self) -> None:
        """Update boss position with smooth movement pattern."""
        self.move_timer += 0.02
        self.rect.x += int(math.cos(self.move_timer) * 1.5)  # Horizontal wave pattern
        self.rect.y += int(math.sin(self.move_timer * 0.8) * 1.2)  # Vertical wave pattern


class Projectile(pygame.sprite.Sprite):
    """Projectile class."""

    def __init__(self, x: int, y: int, velocity: tuple[int, int]) -> None:
        """Projectile constructor."""
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill("yellow")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity

    def update(self) -> None:
        """Update projectile."""
        self.rect.x += self.velocity[0] * 10
        self.rect.y += self.velocity[1] * 10

    def move(self, x: int, y: int) -> None:
        """Move projectile."""
        self.rect.x += x
        self.rect.y += y

    def draw(self) -> None:
        """Draw projectile."""
        pygame.draw.circle(screen, "blue", (self.rect.x, self.rect.y), 10)

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
