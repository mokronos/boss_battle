from enum import Enum


class GameState(Enum):
    """Game states."""

    MAINMENU = "main_menu"
    CONFIG = "config"
    PLAYING = "playing"
