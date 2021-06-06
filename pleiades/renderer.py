from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional
import pygame as pg
from pleiades.prepare import *


class Renderer:

    @staticmethod
    def print(
            string: str,
            color: Optional[Tuple[int, int, int]],
            position: str
        ) -> None:
        screen_pos: Tuple[int, int]
        try:
            screen_pos = getattr(SCREEN_RECT, position)
        except AttributeError:
            print("Invalid position string.")
            screen_pos = SCREEN_RECT.topleft
        _render = FONT.render(string, True, color if color else (255, 255, 255))
        screen.blit(_render, _render.get_rect(center=screen_pos))
