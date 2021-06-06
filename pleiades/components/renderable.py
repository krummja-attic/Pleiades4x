from ecstremity import Component
from typing import Tuple
import pygame
import math

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000


class Renderable(Component):

    def __init__(
            self,
            size: int,
            weight: int,
            color: Tuple[int, int, int],
            has_ellipse: bool = True
        ) -> None:
        self.size = size
        self.weight = weight
        self.color = color
        self.has_ellipse = has_ellipse

    def draw(self, screen):
        pos = self.entity["Position"].position
        # if self.has_ellipse:
        #     ellipse_rect = self.compute_ellipse()
        #     pygame.draw.ellipse(screen, (0, 255, 0), width = 1, rect = ellipse_rect)
        surface = pygame.Surface(SCREEN_SIZE)
        pygame.draw.circle(surface, self.color, (pos.x, pos.y), self.size, self.weight)
        return surface

    def compute_ellipse(self) -> pygame.Rect:
        kepler = self.entity["KeplerElements"]
        parent_pos = self.entity["BaseBody"].parent_entity["Position"].position

        semi_major_axis = kepler.semi_major_axis
        semi_minor_axis = semi_major_axis * math.sqrt(1 - pow(kepler.eccentricity, 2))

        focal_length = math.sqrt(pow(semi_major_axis, 2) - pow(semi_minor_axis, 2))
        x_offset = semi_major_axis + focal_length

        x = parent_pos.x - x_offset
        y = parent_pos.y - semi_minor_axis * kepler.cosI
        w = semi_major_axis * 2
        h = semi_minor_axis * 2 * kepler.cosI

        return pygame.Rect((x, y), (w, h))
