from __future__ import annotations
from typing import *

from ecstremity import Engine, World
import os
import sys
import math
import pygame
import pygame.mixer
import random
import euclid
from euclid import Vector2 as Vec2
from pygame.locals import *
from collections import namedtuple

if TYPE_CHECKING:
    from pygame.surface import Surface, SurfaceType
    from pygame.time import Clock


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
FPS_LIMIT = 60


class ECSManager:

    def __init__(self, client: Client):
        self.engine: Engine = Engine(client)
        self.world: World = self.engine.create_world()


class Client:

    def __init__(self):
        self.dtick: float = 0.0
        self.screen: Union[Surface, SurfaceType] = pygame.display.set_mode(SCREEN_SIZE)
        self.clock: Clock = pygame.time.Clock()
        self.ecs: ECSManager = ECSManager(self)

    def update(self, dt):
        for obj in self.objects:
            obj.move(dt)
            obj.display(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt_ms = self.clock.tick(FPS_LIMIT)
            dt = dt_ms / 1000.0

            self.dtick = dt
            if self.dtick > 1.0:
                self.dtick = 0.0

            self.screen.lock()
            self.screen.fill((21, 21, 21))
            # Update states
            self.screen.unlock()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
