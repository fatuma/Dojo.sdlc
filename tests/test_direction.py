import pytest

from mars_rover.direction import Direction


def test_turning_right_four_times_from_north_goes_through_east_south_west_north():
    headings = []
    direction = Direction.N
    for _ in range(4):
        direction = direction.turn_right()
        headings.append(direction)

    assert headings == [Direction.E, Direction.S, Direction.W, Direction.N]


def test_turning_left_four_times_from_north_goes_through_west_south_east_north():
    headings = []
    direction = Direction.N
    for _ in range(4):
        direction = direction.turn_left()
        headings.append(direction)

    assert headings == [Direction.W, Direction.S, Direction.E, Direction.N]


@pytest.mark.parametrize(
    ("direction", "step"),
    [
        (Direction.N, (0, -1)),
        (Direction.S, (0, 1)),
        (Direction.E, (1, 0)),
        (Direction.W, (-1, 0)),
    ],
)
def test_step_follows_origin_at_top_left_with_north_decreasing_y(direction, step):
    assert direction.step == step
