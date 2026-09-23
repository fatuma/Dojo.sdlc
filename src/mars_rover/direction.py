from enum import Enum


class Direction(Enum):
    """Orientation du rover, déclarée dans l'ordre horaire N → E → S → W."""

    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

    @property
    def step(self) -> tuple[int, int]:
        """Déplacement (dx, dy) d'une case : origine en haut à gauche, N = y décroissant (R-05)."""
        return self.value

    def turn_right(self) -> "Direction":
        return self._rotate(1)

    def turn_left(self) -> "Direction":
        return self._rotate(-1)

    def _rotate(self, quarter_turns: int) -> "Direction":
        clockwise = list(Direction)
        return clockwise[(clockwise.index(self) + quarter_turns) % len(clockwise)]
