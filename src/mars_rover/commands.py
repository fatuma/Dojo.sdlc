from enum import Enum

from mars_rover.errors import InvalidRequest


class Command(Enum):
    """Commandes du rover, avec leur lettre dans le contrat d'API (R-03)."""

    FORWARD = "F"
    RIGHT = "R"
    LEFT = "L"


def parse_commands(text: str) -> list[Command]:
    return [_parse_letter(letter, position) for position, letter in enumerate(text)]


def _parse_letter(letter: str, position: int) -> Command:
    try:
        return Command(letter)
    except ValueError:
        raise InvalidRequest(f"commande inconnue {letter!r} en position {position}") from None
