# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


class Player:
    """Player class."""

    def __init__(self, x: int = 400, y: int = 400) -> None:
        """Player constructor."""
        self.x = x
        self.y = y

    def move(self, x: int, y: int) -> None:
        """Move player."""
        self.x += x
        self.y += y

    def draw(self) -> None:
        """Draw player."""
        pygame.draw.circle(screen, "red", (self.x, self.y), 40)

class Boss:
    """Boss class."""

    def __init__(self, x: int = 100, y: int = 100, health: int = 100) -> None:
        """Boss constructor."""
        self.x = x
        self.y = y
        self.health = health

    def move(self, x: int, y: int) -> None:
        """Move boss."""
        self.x += x
        self.y += y

    def draw(self) -> None:
        """Draw boss."""
        pygame.draw.circle(screen, "green", (self.x, self.y), 40)


class Projectile:
    """Projectile class."""

    def __init__(self, x: int, y: int, velocity: tuple[int, int]) -> None:
        """Projectile constructor."""
        self.x = x
        self.y = y
        self.velocity = velocity

    def update(self) -> None:
        """Update projectile."""
        self.x += self.velocity[0] * 10
        self.y += self.velocity[1] * 10

    def move(self, x: float, y: float) -> None:
        """Move projectile."""
        self.x += x
        self.y += y

    def draw(self) -> None:
        """Draw projectile."""
        pygame.draw.circle(screen, "blue", (self.x, self.y), 10)

updates = []

player = Player(0, 0)
boss = Boss(1000, 1000)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    player.draw()
    boss.draw()

    for update in updates:
        update.update()
        update.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_x]:
        pygame.quit()
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        x_mouse, y_mouse = pygame.mouse.get_pos()
        len_vec = ((x_mouse - player.x) ** 2 + (y_mouse - player.y) ** 2) ** 0.5
        vel = ((x_mouse - player.x) / len_vec, (y_mouse - player.y) / len_vec)
        projectile = Projectile(player.x, player.y, velocity=vel)
        updates.append(projectile)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
