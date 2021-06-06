from __future__ import annotations
from typing import *
import pygame
import math
from morphism import *  # type: ignore

if TYPE_CHECKING:
    from pygame import Surface
    from ecstremity import Entity
    from pleiades.client import Client


class Renderer:

    def __init__(self, client: Client):
        self.client = client

    @staticmethod
    def _prepare_surface(width, height) -> pygame.Surface:
        surface = pygame.Surface((width, height))
        return surface

    @staticmethod
    def compute_ellipse(entity: Entity):
        keplers = entity["KeplerElements"]
        parent = entity["BaseBody"].parent_entity["Position"].xy
        semi_major_axis = keplers.semi_major_axis
        semi_minor_axis = semi_major_axis * math.sqrt(1 - pow(kepler.eccentricity, 2))
        focal_length = math.sqrt(pow(semi_major_axis, 2) - pow(semi_minor_axis, 2))
        x_offset = semi_major_axis + focal_length
        ellipse = pygame.Rect((parent[0] - x_offset, parent[1] - semi_minor_axis),
                              (semi_major_axis * 2), semi_minor_axis * 2)
        return ellipse

    @staticmethod
    def transform(obj: pygame.Surface, angle: float):
        return pygame.transform(obj, angle)

    @staticmethod
    def draw(screen: Surface, target: Surface) -> None:
        pass
