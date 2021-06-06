from __future__ import annotations
from typing import Generic, Optional, Callable
from pleiades import prepare
from pleiades.event import EventDispatch, T, get
import pygame as pg
from pygame import K_RETURN, K_ESCAPE


class StateBreak(Exception):
    """Return None"""


class State(Generic[T], EventDispatch[T]):

    COMMAND_KEYS = {
        K_RETURN: "confirm",
        K_ESCAPE: "quit"
    }
    MOVE_KEYS = {}

    def loop(self) -> Optional[T]:
        while True:

            prepare.screen.fill(prepare.BACKGROUND_COLOR)
            self.on_draw()
            pg.display.update()

            for event in get():
                try:
                    value: T = self.dispatch(event)
                except StateBreak:
                    return None
                if value is not None:
                    return value

    def on_draw(self) -> None:
        raise NotImplementedError()

    def ev_quit(self, event: pg.QUIT) -> Optional[T]:
        return self.cmd_quit()

    def ev_keydown(self, event: pg.KEYDOWN) -> Optional[T]:
        func: Callable[[], Optional[T]]
        key = event.__dict__['key']
        if key in self.COMMAND_KEYS:
            func = getattr(self, f"cmd_{self.COMMAND_KEYS[key]}")
            return func()
        elif key in self.MOVE_KEYS:
            return self.cmd_move(*self.MOVE_KEYS[key])
        return None

    def cmd_confirm(self) -> Optional[T]:
        pass

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_quit(self):
        raise SystemExit()
