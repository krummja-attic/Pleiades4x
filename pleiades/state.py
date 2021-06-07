from __future__ import annotations
from typing import Generic, Optional, Callable, TYPE_CHECKING
from collections import namedtuple
import pygame as pg
import pygame_gui as pgui

# Key inputs
from pygame import (
    K_RETURN,
    K_ESCAPE,
)

# Input events
from pygame import (
    KEYDOWN,
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    USEREVENT,
)

from pleiades import prepare
from pleiades.prepare import SCREEN, BACKGROUND
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
        K_ESCAPE: "escape"
    }
    MOVE_KEYS = {}
    POINTERDATA = PointerData()

    def __init__(self, client: Client):
        self.client = client
        self.client.ui_manager.set_visual_debug_mode(prepare.DEBUG["gui"])
        self.ui_elements = {}

    def register_ui_element(self, key, element):
        self.ui_elements[element] = key

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def handle_input(self):
        for event in pg.event.get():
            try:
                value: T = self.dispatch(event)
                self.client.ui_manager.process_events(event)
            except StateBreak:
                return None
            if value is not None:
                return value

    def update(self, dt: float):
        self.client.ui_manager.update(dt)
        SCREEN.blit(BACKGROUND, (0, 0))
        self.draw(dt)
        self.draw_ui()
        pg.display.update()

    def draw(self, dt: float) -> None:
        raise NotImplementedError()

    def draw_ui(self):
        self.client.ui_manager.draw_ui(SCREEN)
        self._draw_cursor()

    def ev_quit(self, event: QUIT) -> Optional[T]:
        return self.cmd_escape()

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

    def ev_userevent(self, event: USEREVENT) -> Optional[T]:
        if event:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element in self.ui_elements:
                    func = getattr(self, f"ui_{self.ui_elements[event.ui_element]}")
                    return func()

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self) -> Optional[T]:
        raise SystemExit()

    def _draw_cursor(self):
        self.POINTERDATA.cursor = pg.draw.polygon(
            SCREEN,
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

    def _draw_debug(self):
        if prepare.DEBUG["fps"]:
            self._draw_fps()
        if prepare.DEBUG["mouse"]:
            self._draw_mouse_data()

    def _draw_fps(self):
        Renderer.print(str(int(self.client.clock.get_fps())), (255, 255, 255), "topright", -40, 10)

    def _draw_mouse_data(self):
        Renderer.print("    x: " + str(self.POINTERDATA.x), (255, 255, 255), "topleft", 10, 10)
        Renderer.print("    y: " + str(self.POINTERDATA.y), (255, 255, 255), "topleft", 10, 30)
        Renderer.print("click: " + str(self.POINTERDATA.click), (255, 255, 255), "topleft", 10, 50)


