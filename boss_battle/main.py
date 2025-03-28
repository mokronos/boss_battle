import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
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
        pass
        
    def update(self):
        self.rect.x += self.velocity[0] * self.movement_speed
        self.rect.y += self.velocity[1] * self.movement_speed
      
    def handle_event(self, event: pygame.event.Event) -> None:
      
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
          all_sprites.add(Projectile(self.rect.x, self.rect.y, velocity=vel))

class Boss(pygame.sprite.Sprite):
    """Boss class."""

    def __init__(self, x: int, y: int, health: int) -> None:
        """Boss constructor."""
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        self.health = health

    def draw(self) -> None:
        pass
        
    def update(self):
        pass


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

all_sprites.add(Player(0, 0, 10))
all_sprites.add(Boss(500, 500, health=100))

while running:
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
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(144) / 1000

pygame.quit()
