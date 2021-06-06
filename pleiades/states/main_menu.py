from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_gui as pgui

from pleiades import prepare
from pleiades.renderer import Renderer
from pleiades.state import State
from pleiades.states.game import Game

if TYPE_CHECKING:
    from pleiades.client import Client


class MainMenu(State[None]):

    def __init__(self, client: Client):
        super().__init__(client)

        bottom = prepare.SCREEN_RECT.bottom

        panel = pgui.elements.UIPanel(
            relative_rect = pg.Rect((20, bottom - 120), (300, 100)),
            starting_layer_height = 0,
            manager = self.client.gui
        )

        start_game = pgui.elements.UIButton(
            relative_rect = pg.Rect((10, 10), (100, 40)),
            text = "Start",
            manager = self.client.gui,
            container = panel
        )
        self.register_ui_element("start_game", start_game)

    def on_draw(self, dt: float):
        pass

    def ui_start_game(self):
        self.client.push_state(Game)

    def ui_open_window(self):
        pgui.elements.UIWindow(
            rect = pg.Rect((100, 100), (200, 200)),
            manager = self.client.gui,
            window_display_title = "Test"
        )
