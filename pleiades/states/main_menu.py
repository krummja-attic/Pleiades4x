from __future__ import annotations
import pygame as pg
import pygame_gui as pgui

from pleiades.state import State
from pleiades import prepare
from pleiades.renderer import Renderer


class MainMenu(State[None]):

    def __init__(self, client):
        super().__init__(client)

        ui_window = pgui.elements.UIWindow(
            rect = pg.Rect((100, 100), (300, 300)),
            manager = self.gui,
            window_display_title = "Test Window",
        )

    def on_draw(self, dt: float):
        Renderer.print("P L E I A D E S", (255, 0, 0), "center", centered=True)

    def ui_hello_button(self):
        print("Hello!")
