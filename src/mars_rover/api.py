from typing import Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from mars_rover.commands import parse_commands
from mars_rover.direction import Direction
from mars_rover.errors import InvalidRequest
from mars_rover.grid import parse_map
from mars_rover.simulation import RoverState, simulate

app = FastAPI(title="Simulateur Mars Rover")


class SimulationRequest(BaseModel):
    # Contrat R-03 : entiers stricts (ni "3" ni true) et aucun champ en plus (D-03).
    model_config = ConfigDict(strict=True, extra="forbid")

    x: int
    y: int
    direction: Literal["N", "S", "E", "W"]
    rows: list[str] = Field(alias="map")
    commands: str


class SimulationResponse(BaseModel):
    x: int
    y: int
    direction: Literal["N", "S", "E", "W"]
    blocked: bool


@app.post("/simulations")
def run_simulation(request: SimulationRequest) -> SimulationResponse:
    result = simulate(
        grid=parse_map(request.rows),
        start=RoverState(request.x, request.y, Direction[request.direction]),
        commands=parse_commands(request.commands),
    )
    final = result.state
    return SimulationResponse(
        x=final.x, y=final.y, direction=final.direction.name, blocked=result.blocked
    )


@app.exception_handler(InvalidRequest)
def reject_invalid_request(_: Request, error: InvalidRequest) -> JSONResponse:
    return _rejection(error.message)


@app.exception_handler(RequestValidationError)
def reject_malformed_request(_: Request, error: RequestValidationError) -> JSONResponse:
    """Remplace la réponse 422 de FastAPI par le rejet uniforme de R-06."""
    first_error = error.errors()[0]
    field = ".".join(str(part) for part in first_error["loc"] if part != "body")
    return _rejection(f"{field or 'corps'} : {first_error['msg']}")


def _rejection(message: str) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": message})
