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
from pleiades.prepare import background
from pleiades.event import EventDispatch, T, get
from pleiades.renderer import Renderer

if TYPE_CHECKING:
    from pleiades.layouts.layout import Layout
    from pleiades.client import Client


class StateBreak(Exception):
    """Return None"""


class State(Generic[T], EventDispatch[T]):

    COMMAND_KEYS = {
        K_RETURN: "confirm",
        K_ESCAPE: "escape"
    }
    MOVE_KEYS = {}

    def __init__(self, client: Client):
        self.client = client
        self._layout = None

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        self._layout = value
        self._layout.initialize()

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def handle_input(self):
        for event in pg.event.get():
            try:
                value: T = self.dispatch(event)
                self.client.ui.backend.process_events(event)
            except StateBreak:
                return None
            if value is not None:
                return value

    def update(self, dt: float):
        background.fill(prepare.BACKGROUND_COLOR)
        self.client.ui.update(dt)
        pg.display.get_surface().blit(background, (0, 0))
        self.draw(dt)
        self.client.ui.draw()
        pg.display.update()

    def draw(self, dt: float) -> None:
        raise NotImplementedError()

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
        self.client.ui.pointer_data.x = event.pos[0]
        self.client.ui.pointer_data.y = event.pos[1]
        return None

    def ev_mousebuttondown(self, event: MOUSEBUTTONDOWN) -> Optional[T]:
        if event:
            self.client.ui.pointer_data.click = True
        return False

    def ev_mousebuttonup(self, event: MOUSEBUTTONUP) -> Optional[T]:
        if event:
            self.client.ui.pointer_data.click = False
        return False

    def ev_userevent(self, event: USEREVENT) -> Optional[T]:
        if event:
            if event.user_type == pgui.UI_BUTTON_PRESSED:
                match = ''
                for name in event.ui_element.combined_element_ids:
                    if name in self.layout.elements.keys():
                        match = name

                if len(match) > 0:
                    func = getattr(self, f"ui_{match}")
                    return func()

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_escape(self) -> Optional[T]:
        raise SystemExit()

    def _draw_debug(self):
        if prepare.DEBUG["fps"]:
            self._draw_fps()

    def _draw_fps(self):
        Renderer.print(str(int(self.client.clock.get_fps())), (255, 255, 255), "topright", -40, 10)
