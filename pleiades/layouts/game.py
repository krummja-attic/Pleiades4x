from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_gui as pgui
from pygame_gui.elements import *

from pleiades.renderer import Renderer
from pleiades.layouts.layout import Layout
from pleiades import prepare

if TYPE_CHECKING:
    from pleiades.ui_manager import UIManager


class Game(Layout):

    def initialize(self):
        NAVIGATION_PANE_RECT = pg.Rect(0, 0, 160, 115)
        NAVIGATION_PANE_RECT.bottomleft = (20, -20)
        NAVIGATION_PANE = UIPanel(
            relative_rect = NAVIGATION_PANE_RECT,
            starting_layer_height = 0,
            manager = self.client.ui.backend,
            anchors = {
                "left": "left",
                "right": "left",
                "top": "bottom",
                "bottom": "bottom"
            }
        )

        nav_up = UIButton(
            relative_rect = pg.Rect(40, 10, 30, 30),
            text="", manager = self.client.ui.backend,
            container = NAVIGATION_PANE, object_id = "nav_up"
        )

        nav_left = UIButton(
            relative_rect = pg.Rect(10, 40, 30, 30),
            text="", manager = self.client.ui.backend,
            container = NAVIGATION_PANE, object_id = "nav_left"
        )

        nav_down = UIButton(
            relative_rect = pg.Rect(40, 70, 30, 30),
            text="", manager = self.client.ui.backend,
            container = NAVIGATION_PANE, object_id = "nav_down"
        )

        nav_right = UIButton(
            relative_rect = pg.Rect(70, 40, 30, 30),
            text="", manager = self.client.ui.backend,
            container = NAVIGATION_PANE, object_id = "nav_right"
        )

        zoom_in = UIButton(
            relative_rect = pg.Rect(115, 10, 30, 30),
            text="", manager = self.client.ui.backend,
            container = NAVIGATION_PANE, object_id = "zoom_in"
        )

        zoom_out = UIButton(
            relative_rect = pg.Rect(115, 70, 30, 30),
            text = "", manager = self.client.ui.backend,
            container = NAVIGATION_PANE, object_id = "zoom_out"
        )

        self.register("nav_up", nav_up)
        self.register("nav_down", nav_down)
        self.register("nav_left", nav_left)
        self.register("nav_right", nav_right)
        self.register("zoom_in", zoom_in)
        self.register("zoom_out", zoom_out)
