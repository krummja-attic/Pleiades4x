from __future__ import annotations
import pygame as pg
from pygame.locals import *

from pleiades import prepare
from pleiades.state import State


class Client:

    def __init__(self):
        self.clock = pg.time.Clock()
        self.states = {}
        self.current_state = None

    def initialize(self, key: str, state: State) -> None:
        self.states[key] = state
        self.current_state = state

    def run(self):
        running = True
        while running:
            self.current_state.loop()
