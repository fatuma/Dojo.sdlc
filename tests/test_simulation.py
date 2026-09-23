import pytest

from mars_rover.commands import parse_commands
from mars_rover.direction import Direction
from mars_rover.errors import InvalidRequest
from mars_rover.grid import parse_map
from mars_rover.simulation import RoverState, SimulationResult, simulate

OPEN_3_BY_3 = parse_map(["🟩🟩🟩", "🟩🟩🟩", "🟩🟩🟩"])
CENTER_FACING_NORTH = RoverState(1, 1, Direction.N)


def run(grid, start, commands):
    return simulate(grid, start, parse_commands(commands))


def test_moving_forward_facing_north_decrements_y_and_keeps_heading():
    result = run(OPEN_3_BY_3, CENTER_FACING_NORTH, "F")

    assert result == SimulationResult(RoverState(1, 0, Direction.N), blocked=False)


@pytest.mark.parametrize(
    ("commands", "final_state"),
    [
        ("RF", RoverState(2, 1, Direction.E)),
        ("FR", RoverState(1, 0, Direction.E)),
    ],
)
def test_commands_run_in_list_order(commands, final_state):
    assert run(OPEN_3_BY_3, CENTER_FACING_NORTH, commands).state == final_state


def test_obstacle_ahead_stops_the_rover_and_skips_remaining_commands():
    grid = parse_map(["🟩🌳", "🟩🟩"])
    start = RoverState(0, 0, Direction.E)

    assert run(grid, start, "FLF") == SimulationResult(start, blocked=True)


def test_no_command_returns_the_starting_state_unblocked():
    assert run(OPEN_3_BY_3, CENTER_FACING_NORTH, "") == SimulationResult(
        CENTER_FACING_NORTH, blocked=False
    )


@pytest.mark.parametrize(
    ("start", "commands"),
    [
        (RoverState(1, 0, Direction.N), "F"),
        (RoverState(1, 2, Direction.S), "F"),
        (RoverState(2, 1, Direction.E), "F"),
        (RoverState(0, 1, Direction.W), "F"),
        (RoverState(0, 0, Direction.E), "FFF"),
    ],
)
def test_leaving_the_map_rejects_the_request(start, commands):
    with pytest.raises(InvalidRequest, match="sortir le rover de la carte"):
        run(OPEN_3_BY_3, start, commands)


def test_obstacle_met_before_leaving_the_map_gives_a_blocked_result():
    grid = parse_map(["🟩🟩🌳"])

    result = run(grid, RoverState(0, 0, Direction.E), "FFLF")

    assert result == SimulationResult(RoverState(1, 0, Direction.E), blocked=True)


def test_start_outside_the_map_is_rejected():
    with pytest.raises(InvalidRequest, match="hors de la carte"):
        run(OPEN_3_BY_3, RoverState(3, 0, Direction.N), "")


def test_start_on_an_obstacle_is_rejected():
    grid = parse_map(["🌳🟩"])

    with pytest.raises(InvalidRequest, match="sur un obstacle"):
        run(grid, RoverState(0, 0, Direction.N), "")
