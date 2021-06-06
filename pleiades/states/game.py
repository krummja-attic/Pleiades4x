from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_gui as pgui

from pleiades.state import State
from pleiades import prepare
from pleiades.renderer import Renderer

if TYPE_CHECKING:
    from pleiades.client import Client


class Game(State[None]):

    def __init__(self, client: Client):
        super().__init__(client)

    def on_draw(self, dt: float):
        Renderer.print("Game Screen", (255, 255, 255), "topleft")
