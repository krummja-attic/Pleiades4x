from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Optional
import pygame as pg
from pleiades.prepare import *


class Renderer:

    @staticmethod
    def print(
            string: str,
            color: Optional[Tuple[int, int, int]],
            position: str,
            x_offset: int = 0,
            y_offset: int = 0,
            centered: bool = False
        ) -> None:
        screen_pos: Tuple[int, int]

        try:
            _screen_pos = getattr(SCREEN_RECT, position)
        except AttributeError:
            print("Invalid position string.")
            _screen_pos = SCREEN_RECT.topleft

        screen_pos = (_screen_pos[0] + x_offset, _screen_pos[1] + y_offset)
        _render = FONT.render(string, True, color if color else (255, 255, 255))

        if centered:
            WINDOW_SURFACE.blit(_render, _render.get_rect(center=screen_pos))
        else:
            WINDOW_SURFACE.blit(_render, _render.get_rect(topleft=screen_pos))
