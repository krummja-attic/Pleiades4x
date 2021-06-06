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
        self.stack = []
        self.current_state = None
        self.clock = pg.time.Clock()
        self.gui = pgui.UIManager(prepare.SCREEN_SIZE)

    def initialize(self, key: str, state: Type[State]) -> None:
        self.states[key] = state
        self.current_state = state(self)
        self.push_state(state)

    def push_state(self, state: Type[State]) -> None:
        self.gui.clear_and_reset()
        self.stack.append(state(self))
        self.current_state.on_enter()

    def pop_state(self):
        state = self.stack.pop()
        state.on_leave()

    def clear_stack(self):
        while len(self.stack) > 1:
            self.stack.pop()

    def set_state(self, state: Type[State]):
        self.clear_stack()
        self.push_state(state)

    def run(self):
        running = True
        while running:
            self.current_state = self.stack[-1]
            self.current_state.loop()
