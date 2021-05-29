from __future__ import annotations
from typing import *

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


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, WHITE, RED, GREEN, BLUE]

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
FPS_LIMIT = 60


class Circle:

    def __init__(
            self,
            position: Vec2,
            radius: int,
            color: Tuple[int, int, int] = WHITE,
            velocity: euclid.Vector2 = Vec2(0, 0)
        ) -> None:
        self.position = position
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def display(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=self.position,
            radius=self.radius,
            width=1
        )

    def move(self, dt: float) -> None:
        self.position += self.velocity * dt

    def change_velocity(self, velocity: Vec2) -> None:
        self.velocity = velocity


def get_random_velocity(initial: int = 20) -> Vec2:
    new_angle = random.uniform(0, math.pi * 2)
    new_x = math.sin(new_angle)
    new_y = math.cos(new_angle)
    new_vector = Vec2(new_x, new_y)
    new_vector.normalize()
    new_vector *= initial
    return new_vector


class Client:

    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.objects = []
        self.dtick = 0.0

    def initialize(self, count: int = 1, min_size: int = 10, max_size: int = 40):
        for n in range(count):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randrange(min_size, max_size)
            color = random.choice(COLORS)
            velocity = get_random_velocity()
            self.objects.append(Circle(Vec2(x, y), radius, color, velocity))

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
                random_circle = random.choice(self.objects)
                new_velocity = get_random_velocity()
                random_circle.change_velocity(new_velocity)

            self.screen.lock()
            self.screen.fill(WHITE)
            self.update(dt)
            self.screen.unlock()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
