from dataclasses import dataclass, replace

from mars_rover.commands import Command
from mars_rover.direction import Direction
from mars_rover.errors import InvalidRequest
from mars_rover.grid import Grid


@dataclass(frozen=True)
class RoverState:
    x: int
    y: int
    direction: Direction

    def cell_ahead(self) -> tuple[int, int]:
        dx, dy = self.direction.step
        return self.x + dx, self.y + dy

    def turned_right(self) -> "RoverState":
        return replace(self, direction=self.direction.turn_right())

    def turned_left(self) -> "RoverState":
        return replace(self, direction=self.direction.turn_left())

    def moved_to(self, cell: tuple[int, int]) -> "RoverState":
        x, y = cell
        return replace(self, x=x, y=y)


@dataclass(frozen=True)
class SimulationResult:
    state: RoverState
    blocked: bool


def simulate(grid: Grid, start: RoverState, commands: list[Command]) -> SimulationResult:
    """Exécute tout le trajet avant de répondre : une sortie de carte rejette la demande (R-01, R-06).

    Le premier obstacle arrête le rover et ignore les commandes restantes (R-04).
    """
    _require_valid_start(grid, start)
    state = start
    for position, command in enumerate(commands):
        if command is Command.RIGHT:
            state = state.turned_right()
        elif command is Command.LEFT:
            state = state.turned_left()
        else:
            target = _cell_ahead_within_map(grid, state, position)
            if grid.is_obstacle(*target):
                return SimulationResult(state, blocked=True)
            state = state.moved_to(target)
    return SimulationResult(state, blocked=False)


def _cell_ahead_within_map(grid: Grid, state: RoverState, position: int) -> tuple[int, int]:
    x, y = state.cell_ahead()
    if not grid.contains(x, y):
        raise InvalidRequest(
            f"la commande en position {position} ferait sortir le rover de la carte en ({x}, {y})"
        )
    return x, y


def _require_valid_start(grid: Grid, start: RoverState) -> None:
    if not grid.contains(start.x, start.y):
        raise InvalidRequest(f"le départ ({start.x}, {start.y}) est hors de la carte")
    if grid.is_obstacle(start.x, start.y):
        raise InvalidRequest(f"le départ ({start.x}, {start.y}) est sur un obstacle")
