import pygame

from boss_battle.game_context import GameContext
from boss_battle.types_ import GameState
from boss_battle.sprites.boss import Boss
from boss_battle.sprites.stats import Stats

class ConfigMenu:
    """Config menu with config options."""

    def __init__(self, game_context: GameContext) -> None:
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.game_context = game_context
        self.boss_health = 1000

    def draw(self, screen: pygame.Surface) -> None:
        """Draw menu with start and quit buttons."""
        screen.fill("purple")
        # Title
        text = self.font.render("BOSS BATTLE", True, "white")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 100))

        # Boss health config input
        self.boss_health_input_rect = pygame.Rect(1280 // 2 - 100, 200, 200, 50)
        pygame.draw.rect(screen, "white", self.boss_health_input_rect)
        text = self.small_font.render(str(self.boss_health), True, "black")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 210))

        # Up button to increase boss health
        self.up_button_rect = pygame.Rect(1280 // 2 + 120, 200, 50, 50)
        pygame.draw.rect(screen, "green", self.up_button_rect)
        up_text = self.small_font.render("+", True, "white")
        screen.blit(up_text, (1280 // 2 + 140, 210))

        # Down button to decrease boss health
        self.down_button_rect = pygame.Rect(1280 // 2 - 170, 200, 50, 50)
        pygame.draw.rect(screen, "red", self.down_button_rect)
        down_text = self.small_font.render("-", True, "white")
        screen.blit(down_text, (1280 // 2 - 150, 210))

        # Start button
        self.start_rect = pygame.Rect(1280 // 2 - 100, 300, 200, 50)
        pygame.draw.rect(screen, "green", self.start_rect)
        text = self.small_font.render("START BATTLE", True, "white")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 310))

        # Quit button
        self.quit_rect = pygame.Rect(1280 // 2 - 100, 400, 200, 50)
        pygame.draw.rect(screen, "red", self.quit_rect)
        text = self.small_font.render("MAIN MENU", True, "white")
        screen.blit(text, (1280 // 2 - text.get_width() // 2, 410))

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle user input."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                self.game_context.game_settings["boss_health"] = self.boss_health
                boss = Boss(
                    x=640,
                    y=360,
                    game_context=self.game_context,
                    stats=Stats(health=self.game_context.game_settings.get("boss_health", 500), damage=5, attack_speed=1, movement_speed=2),
                )
                self.game_context.sprites_handler.all_sprites.add(boss)
                self.game_context.sprites_handler.boss_sprites.add(boss)
                self.game_context.game_state = GameState.PLAYING
            elif self.quit_rect.collidepoint(event.pos):
                self.game_context.game_state = GameState.MAINMENU
            elif self.up_button_rect.collidepoint(event.pos):
                self.boss_health += 100  # Increase health by 100
            elif self.down_button_rect.collidepoint(event.pos):
                self.boss_health = max(0, self.boss_health - 100)  # Decrease health by 100, prevent negative health
