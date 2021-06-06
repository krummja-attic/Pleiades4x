from __future__ import annotations
from typing import *
from euclid import Vector3
import math

import pygame

from dataclasses import dataclass

from pleiades.systems import BaseSystem

if TYPE_CHECKING:
    from ecstremity import Entity
    from pleiades.client import Client

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000


class RenderSystem(BaseSystem):

    def initialize(self):
        self.query(key = "bodies", all_of = ["Renderable"])

    def update(self, time: float, scale: float, position: Tuple[int, int]):
        bodies = self._queries["bodies"].result
        for body in bodies:
            surface = body["Renderable"].draw(self.client.screen)
            surface = pygame.transform.scale(surface, (int(SCREEN_WIDTH * scale), int(SCREEN_HEIGHT * scale)))
            surface.set_colorkey(pygame.Color(0, 0, 0))
            self.client.screen.blit(surface, position)
