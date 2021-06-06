from __future__ import annotations
import pygame as pg

from pleiades.state import State
from pleiades import prepare
from pleiades.renderer import Renderer


class MainMenu(State):

    def on_draw(self, dt: float):
        Renderer.print("P L E I A D E S", (255, 0, 0), "center", centered=True)
