class Stats:
    """Stats for sprites in the game."""

    def __init__(
        self, health: int, damage: int, attack_speed: int, movement_speed: int
    ) -> None:
        self.health = health
        self.max_health = health
        self.damage = damage
        self.movement_speed = movement_speed
        self.attack_speed = attack_speed
