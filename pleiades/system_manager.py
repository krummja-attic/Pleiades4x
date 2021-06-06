from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from pleiades.client import Client


@dataclass
class KeplerData:
    semi_major_axis: float
    eccentricity: float
    inclination: float = 0.0
    swivel: float = 0.0
    position: float = 0.0
    offset: float = 0.0
    anomaly: float = 0.0


class SystemManager:

    def __init__(self, client: Client) -> None:
        self.client = client

    def generate_system(self):
        pass
