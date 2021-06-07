from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_gui as pgui
from pygame_gui.elements import *

from pleiades.prepare import *

if TYPE_CHECKING:
    from pleiades.client import Client


class PointerData:
    cursor: Optional[pg.Rect] = None
    scale: int = 5
    x: int = 0
    y: int = 0
    click: bool = False


class UIManager:

    def __init__(self, client: Client) -> None:
        self.client = client
        self.pointer_data = PointerData()
        self.backend = pgui.UIManager(SCREEN_SIZE, "assets/theme.json")
        self.backend.set_visual_debug_mode(DEBUG["gui"])

    def update(self, dt: float):
        self.backend.update(dt)

    def draw(self):
        self.backend.draw_ui(pg.display.get_surface())
        self.draw_cursor()

    def draw_cursor(self):
        self.pointer_data.cursor = pg.draw.polygon(
            pg.display.get_surface(),
            (255, 0, 0),
            [
                (self.pointer_data.x,
                 self.pointer_data.y),
                (self.pointer_data.x
                 + (2 * self.pointer_data.scale),
                 self.pointer_data.y
                 + (2 * self.pointer_data.scale)),
                (self.pointer_data.x,
                 self.pointer_data.y
                 + (3 * self.pointer_data.scale)),
            ],
            width = 1
        )
