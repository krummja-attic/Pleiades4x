from __future__ import annotations
from typing import *

from pleiades.systems import BaseSystem

if TYPE_CHECKING:
    from pleiades.client import Client


class OrbitSystem(BaseSystem):

    def __init__(self, client: Client):
        super().__init__(client)

    def initialize(self):
        pass

    def update(self):
        pass
