import pytest

from mars_rover.commands import Command, parse_commands
from mars_rover.errors import InvalidRequest


def test_letters_are_read_in_order():
    assert parse_commands("FRL") == [Command.FORWARD, Command.RIGHT, Command.LEFT]


def test_empty_text_gives_no_command():
    assert parse_commands("") == []


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("FX", "commande inconnue 'X' en position 1"),
        ("f", "commande inconnue 'f' en position 0"),
    ],
)
def test_unknown_letter_is_rejected_with_its_position(text, message):
    with pytest.raises(InvalidRequest) as error:
        parse_commands(text)

    assert error.value.message == message
