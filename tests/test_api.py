import pytest
from fastapi.testclient import TestClient

from mars_rover.api import app

client = TestClient(app)

MAP = ["🟩🟩🌳🟩", "🟫🌳🟫🟫"]


def request_body(**overrides):
    body = {"x": 0, "y": 0, "direction": "E", "map": MAP, "commands": "FRL"}
    body.update(overrides)
    return body


def assert_rejected(response):
    assert response.status_code == 400
    assert list(response.json()) == ["error"]
    assert response.json()["error"]


def test_valid_request_returns_final_position_and_direction():
    response = client.post("/simulations", json=request_body())

    assert response.status_code == 200
    assert response.json() == {"x": 1, "y": 0, "direction": "E", "blocked": False}


def test_obstacle_is_reported_as_blocked():
    response = client.post("/simulations", json=request_body(commands="RFLF"))

    assert response.json() == {"x": 0, "y": 1, "direction": "E", "blocked": True}


def test_no_command_returns_the_starting_position():
    response = client.post("/simulations", json=request_body(direction="N", commands=""))

    assert response.json() == {"x": 0, "y": 0, "direction": "N", "blocked": False}


@pytest.mark.parametrize(
    "overrides",
    [
        pytest.param({"direction": "X"}, id="orientation inconnue"),
        pytest.param({"x": "0"}, id="x en chaîne"),
        pytest.param({"y": True}, id="y booléen"),
        pytest.param({"x": 0.5}, id="x décimal"),
        pytest.param({"map": "🟩🟩"}, id="carte en chaîne"),
        pytest.param({"speed": 2}, id="champ inconnu"),
        pytest.param({"map": ["🟩🟩🟩🟩", "🟩🟩🟩"]}, id="carte irrégulière"),
        pytest.param({"map": []}, id="carte vide"),
        pytest.param({"map": ["🟩.🟩🟩", "🟩🟩🟩🟩"]}, id="symbole inconnu"),
        pytest.param({"commands": "FX"}, id="commande inconnue"),
        pytest.param({"x": 9}, id="départ hors carte"),
        pytest.param({"x": 2}, id="départ sur obstacle"),
        pytest.param({"direction": "N", "commands": "F"}, id="sortie de carte"),
    ],
)
def test_invalid_request_is_rejected_without_any_position(overrides):
    assert_rejected(client.post("/simulations", json=request_body(**overrides)))


def test_missing_field_is_rejected():
    body = request_body()
    del body["commands"]

    assert_rejected(client.post("/simulations", json=body))


def test_malformed_json_is_rejected():
    response = client.post(
        "/simulations", content='{"x": 0,', headers={"Content-Type": "application/json"}
    )

    assert_rejected(response)
