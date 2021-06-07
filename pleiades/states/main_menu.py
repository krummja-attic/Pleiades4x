from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_gui as pgui

from pleiades.states.state import State
from pleiades.states.game import Game
from pleiades.layouts import main_menu

if TYPE_CHECKING:
    from pleiades.client import Client


class MainMenu(State[None]):

    def __init__(self, client: Client):
        super().__init__(client)

    def on_enter(self):
        self.layout = main_menu.MainMenu(self.client)

    def draw(self, dt: float):
        pass

    def ui_start_game(self):
        self.client.push_state(Game)

    def ui_open_window(self):
        pgui.elements.UIWindow(
            rect = pg.Rect((100, 100), (200, 200)),
            manager = self.client.ui.backend,
            window_display_title = "Test"
        )
