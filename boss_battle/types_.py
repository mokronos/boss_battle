from enum import Enum


class GameState(Enum):
    """Game states."""

    MAINMENU = "main_menu"
    CONFIGMENU = "config"
    PLAYING = "playing"
