from dataclasses import dataclass

from mars_rover.errors import InvalidRequest

# Jeux A et B de R-02, mélangeables dans une même carte.
FREE_SYMBOLS = frozenset({"\U0001F7E9", "\U0001F7EB"})  # 🟩 🟫
OBSTACLE_SYMBOLS = frozenset({"\U0001F333", "\U0001FAA8"})  # 🌳 🪨


@dataclass(frozen=True)
class Grid:
    width: int
    height: int
    obstacles: frozenset[tuple[int, int]]

    def contains(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle(self, x: int, y: int) -> bool:
        return (x, y) in self.obstacles


def parse_map(rows: list[str]) -> Grid:
    """Traduit une carte en grille, une case par caractère Unicode (D-04)."""
    if not rows:
        raise InvalidRequest("la carte est vide")
    obstacle_rows = [_parse_row(row, y) for y, row in enumerate(rows)]
    _require_rectangular(obstacle_rows)
    return Grid(
        width=len(obstacle_rows[0]),
        height=len(obstacle_rows),
        obstacles=frozenset(
            (x, y)
            for y, row in enumerate(obstacle_rows)
            for x, is_obstacle in enumerate(row)
            if is_obstacle
        ),
    )


def _parse_row(row: str, y: int) -> list[bool]:
    if not row:
        raise InvalidRequest(f"la rangée {y} est vide")
    return [_is_obstacle_symbol(symbol, x, y) for x, symbol in enumerate(row)]


def _is_obstacle_symbol(symbol: str, x: int, y: int) -> bool:
    if symbol in OBSTACLE_SYMBOLS:
        return True
    if symbol in FREE_SYMBOLS:
        return False
    raise InvalidRequest(f"symbole inconnu U+{ord(symbol):04X} en rangée {y}, colonne {x}")


def _require_rectangular(obstacle_rows: list[list[bool]]) -> None:
    expected_width = len(obstacle_rows[0])
    for y, row in enumerate(obstacle_rows):
        if len(row) != expected_width:
            raise InvalidRequest(
                f"la rangée {y} compte {len(row)} cases au lieu de {expected_width}"
            )
