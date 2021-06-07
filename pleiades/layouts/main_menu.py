from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_gui as pgui

from pleiades.renderer import Renderer
from pleiades.layouts.layout import Layout
from pleiades import prepare

if TYPE_CHECKING:
    from pleiades.ui_manager import UIManager


class MainMenu(Layout):

    def initialize(self):
        bottom = prepare.SCREEN_RECT.bottom
        panel = pgui.elements.UIPanel(
            relative_rect = pg.Rect((20, bottom - 120), (300, 100)),
            starting_layer_height = 0,
            manager = self.client.ui.backend
        )
        start_game = pgui.elements.UIButton(
            relative_rect = pg.Rect((10, 10), (100, 40)),
            text = "START",
            manager = self.client.ui.backend,
            container = panel,
            object_id = "start_game"
        )
        self.register("start_game", start_game)
