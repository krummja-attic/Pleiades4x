from __future__ import annotations
from typing import Type
import pygame as pg
import pygame_gui as pgui
from pygame.locals import *

from pleiades import prepare
from pleiades.state import State


class Client:

    def __init__(self):
        self.states = {}
        self.current_state = None
        self.clock = pg.time.Clock()

    def initialize(self, key: str, state: Type[State]) -> None:
        self.states[key] = state
        self.current_state = state(self)

    def run(self):
        running = True
        while running:
            self.current_state.loop()
