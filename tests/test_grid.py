import pytest

from mars_rover.errors import InvalidRequest
from mars_rover.grid import parse_map

SET_A_MAP = ["🟩🟩🌳🟩", "🟩🌳🟩🟩"]
SET_B_MAP = ["🟫🟫🪨🟫", "🟫🪨🟫🟫"]
MIXED_MAP = ["🟩🟫🪨🟩", "🟫🌳🟩🟫"]


def test_both_symbol_sets_and_a_mix_describe_the_same_grid():
    assert parse_map(SET_A_MAP) == parse_map(SET_B_MAP) == parse_map(MIXED_MAP)


def test_grid_locates_obstacles_with_origin_at_top_left():
    grid = parse_map(SET_A_MAP)

    assert grid.is_obstacle(2, 0)
    assert grid.is_obstacle(1, 1)
    assert not grid.is_obstacle(0, 0)
    assert not grid.is_obstacle(3, 1)


@pytest.mark.parametrize(
    ("x", "y", "inside"),
    [
        (0, 0, True),
        (3, 1, True),
        (-1, 0, False),
        (4, 0, False),
        (0, -1, False),
        (0, 2, False),
    ],
)
def test_grid_contains_only_cells_of_the_map(x, y, inside):
    assert parse_map(SET_A_MAP).contains(x, y) is inside


def test_map_with_rows_of_different_lengths_is_rejected():
    with pytest.raises(InvalidRequest, match="rangée 1"):
        parse_map(["🟩🟩🟩🟩", "🟩🟩🟩"])


@pytest.mark.parametrize("rows", [[], ["🟩", ""]])
def test_empty_map_or_empty_row_is_rejected(rows):
    with pytest.raises(InvalidRequest):
        parse_map(rows)


def test_unknown_symbol_is_rejected():
    with pytest.raises(InvalidRequest, match="symbole inconnu"):
        parse_map(["🟩.🟩"])


def test_variation_selector_after_a_symbol_is_rejected_with_its_position():
    with pytest.raises(InvalidRequest) as error:
        parse_map(["🟩🟩🟩", "🌳️🟩"])

    assert error.value.message == "symbole inconnu U+FE0F en rangée 1, colonne 1"
