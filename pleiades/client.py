from __future__ import annotations
from typing import *
import os
import sys
import math
import json
import datetime

import pygame
from pygame import *

from dataclasses import dataclass
from ecstremity import Engine, World
from pygame.locals import *
from euclid import Vector3

from pleiades.components import all_components
from pleiades.systems.orbit_system import OrbitSystem
from pleiades.systems.render_system import RenderSystem
from pleiades.system_manager import SystemManager

from pleiades.utils.constants import Units

if TYPE_CHECKING:
    from ecstremity import Entity
    from pygame.surface import Surface, SurfaceType
    from pygame.time import Clock


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
FPS_LIMIT = 60


class ECSManager:

    def __init__(self, client: Client):
        self.engine: Engine = Engine(client)
        self.world: World = self.engine.create_world()

    def initialize(self):
        for component in all_components():
            self.engine.register_component(component)

        prefab_path = os.path.join("prefabs/")
        prefabs = [f for f in os.listdir(prefab_path) if f.endswith(".json")]
        prefabs.sort()
        for prefab in prefabs:
            with open(prefab_path + prefab) as f:
                definition = json.load(f)
                self.engine.prefabs.register(definition)


@dataclass
class Kepler:
    semi_major_axis: float
    eccentricity: float
    inclination: float = 0.0
    swivel: float = 0.0
    position: float = 0.0
    offset: float = 0.0
    anomaly: float = 0.0
    mass: float = 100.0


class Client:

    def __init__(self):
        self.speed_mult: int = 6000
        self.dtick: float = 0.0
        self.screen: Union[Surface, SurfaceType] = pygame.display.set_mode(SCREEN_SIZE)
        self.clock: Clock = pygame.time.Clock()

        pygame.font.init()
        self.text_display = pygame.font.SysFont('lato', 14)

        self.ecs: ECSManager = ECSManager(self)
        self.ecs.initialize()

        self.system_manager = SystemManager(self)

        self.orbit_system = OrbitSystem(self)
        self.render_system = RenderSystem(self)

        self.stars = []
        self.planets = []

    def initialize(self):
        star = self.ecs.world.create_prefab("celestial", {
            "position": {
                "x": 1000, "y": 1000, "z": 0,
                "system_uid": "test"
            },
            "mass": {
                "value": 100.0
            },
            "renderable": {
                "size": 4,
                "weight": 0,
                "color": (255, 255, 0),
                "has_ellipse": False
            }
        })

        keplers = [
            Kepler(120.0, 0.0, mass = 100.0),
        ]

        for i in range(len(keplers)):
            kepler = keplers[i]
            planet = self.ecs.world.create_prefab("planet", {
                "basebody": {
                    "parent": star.uid
                },
                "position": {
                    "system_uid": "test"
                },
                "mass": {
                    "value": kepler.mass
                },
                "keplerelements": {
                    "semi_major_axis": kepler.semi_major_axis,
                    "eccentricity": kepler.eccentricity,
                    "inclination": kepler.inclination,
                    "swivel": kepler.swivel,
                    "position": kepler.position,
                    "offset": kepler.offset,
                    "anomaly": kepler.anomaly
                },
                "renderable": {
                    "size": 4,
                    "weight": 0,
                    "color": (200, 40, 255),
                    "has_ellipse": True
                }
            })
            self.planets.append(planet)

    def run(self):
        px = 0.0
        py = 0.0

        sx, sy = self.screen.get_size()
        wx, wy = 4000, 4000

        scale = 1.0
        while not any(e.type == KEYDOWN and e.key == K_ESCAPE for e in event.get()):

            dt = 0.001 * self.clock.tick()

            self.dtick = dt
            if self.dtick > 1.0:
                self.dtick = 0.0

            k = key.get_pressed()

            if k[K_KP_PLUS]:
                scale += 0.01
            if k[K_KP_MINUS]:
                scale -= 0.01

            px += (k[K_RIGHT] - k[K_LEFT]) * 1000 * dt
            py += (k[K_DOWN] - k[K_UP]) * 1000 * dt

            px = min(max(px, 0), wx)
            py = min(max(py, 0), wy)

            cx = min(max(px, sx // 2), wx - sx // 2)
            cy = min(max(py, sy // 2), wy - sy // 2)

            if scale <= 0.0:
                scale = 0.1

            self.screen.fill((0, 0, 64))

            self.orbit_system.update(pygame.time.get_ticks() * self.speed_mult)
            self.render_system.update(pygame.time.get_ticks() * self.speed_mult, scale, (sx // 2 - cx, sy // 2 - cy))

            # Debug Display Info
            fps_display = self.text_display.render("FPS: " + str(int(self.clock.get_fps())), False, (255, 255, 255))
            self.screen.blit(fps_display, (10, 10))

            epoch = datetime.datetime.now()
            epoch_string = epoch.strftime("%Y/%m/%d %H:%M:%S")
            epoch_display = self.text_display.render("Epoch: " + epoch_string, False, (255, 255, 255))
            self.screen.blit(epoch_display, (10, 40))

            scale_display = self.text_display.render("Scale: " + str(scale), False, (255, 255, 255))
            self.screen.blit(scale_display, (10, 60))

            position_display = self.text_display.render("Position: " + str((px, py)), False, (255, 255, 255))
            self.screen.blit(position_display, (10, 80))

            draw.circle(self.screen, (255, 0, 0), (int(sx // 2 + px - cx), int(sy // 2 + py - cy)), 5, width = 1)

            # Display Flip
            pygame.display.flip()

        pygame.quit()
        sys.exit()
