import pygame

from boss_battle.game_context import GameContext


class Menu:
    """Main menu with start and quit buttons."""

    def __init__(self, game_context: GameContext) -> None:
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.game_state = "menu"
        self.game_context = game_context

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
