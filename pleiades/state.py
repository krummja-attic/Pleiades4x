from __future__ import annotations
from typing import Generic, Optional, Callable, TYPE_CHECKING
from collections import namedtuple
import pygame as pg
from pygame import (K_RETURN, K_ESCAPE, KEYDOWN, QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP)

from pleiades import prepare
from pleiades.event import EventDispatch, T, get
from pleiades.renderer import Renderer

if TYPE_CHECKING:
    from pleiades.client import Client


class StateBreak(Exception):
    """Return None"""


class PointerData:
    cursor: Optional[pg.Rect] = None
    scale: int = 5
    x: int = 0
    y: int = 0
    click: bool = False


class State(Generic[T], EventDispatch[T]):

    COMMAND_KEYS = {
        K_RETURN: "confirm",
        K_ESCAPE: "quit"
    }
    MOVE_KEYS = {}
    POINTERDATA = PointerData()

    def __init__(self, client: Client):
        self.client = client

    def loop(self) -> Optional[T]:
        while True:

            prepare.screen.fill(prepare.BACKGROUND_COLOR)
            dt = 0.001 * self.client.clock.tick()
            self.on_draw(dt)
            self._draw_cursor()
            self._draw_mouse_data()
            self._draw_fps()
            pg.display.update()

            for event in get():
                try:
                    value: T = self.dispatch(event)
                except StateBreak:
                    return None
                if value is not None:
                    return value

    def _draw_mouse_data(self):
        Renderer.print("    x: " + str(self.POINTERDATA.x), (255, 255, 255), "topleft", 10, 10)
        Renderer.print("    y: " + str(self.POINTERDATA.y), (255, 255, 255), "topleft", 10, 30)
        Renderer.print("click: " + str(self.POINTERDATA.click), (255, 255, 255), "topleft", 10, 50)

    def _draw_fps(self):
        Renderer.print(str(int(self.client.clock.get_fps())), (255, 255, 255), "topright", -40, 10)

    def _draw_cursor(self):
        self.POINTERDATA.cursor = pg.draw.polygon(
            prepare.screen,
            (255, 0, 0),
            [
                (self.POINTERDATA.x,
                 self.POINTERDATA.y),
                (self.POINTERDATA.x
                 + (2 * self.POINTERDATA.scale),
                 self.POINTERDATA.y
                 + (2 * self.POINTERDATA.scale)),
                (self.POINTERDATA.x,
                 self.POINTERDATA.y
                 + (3 * self.POINTERDATA.scale)),
            ],
            width = 1
        )

    def on_draw(self, dt: float) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: QUIT) -> Optional[T]:
        return self.cmd_quit()

    def ev_keydown(self, event: KEYDOWN) -> Optional[T]:
        func: Callable[[], Optional[T]]
        key = event.__dict__['key']
        if key in self.COMMAND_KEYS:
            func = getattr(self, f"cmd_{self.COMMAND_KEYS[key]}")
            return func()
        elif key in self.MOVE_KEYS:
            return self.cmd_move(*self.MOVE_KEYS[key])
        return None

    def ev_mousemotion(self, event: MOUSEMOTION) -> Optional[T]:
        self.POINTERDATA.x = event.pos[0]
        self.POINTERDATA.y = event.pos[1]
        return None

    def ev_mousebuttondown(self, event: MOUSEBUTTONDOWN) -> Optional[T]:
        if event:
            self.POINTERDATA.click = True
        return False

    def ev_mousebuttonup(self, event: MOUSEBUTTONUP) -> Optional[T]:
        if event:
            self.POINTERDATA.click = False
        return False

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_quit(self):
        raise SystemExit()
