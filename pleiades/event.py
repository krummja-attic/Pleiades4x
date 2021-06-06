from __future__ import annotations
from typing import *
import pygame as pg
from pygame import KEYDOWN, QUIT, KEYUP

T = TypeVar("T")


def get() -> Iterator[Any]:
    return pg.event.get()


class EventDispatch(Generic[T]):

    def dispatch(self, event: Any) -> Optional[T]:
        event_type = pg.event.event_name(event.type)
        if event_type is None:
            return None
        if event_type in [
            "KeyDown",
            "Quit",
            "MouseMotion",
            "MouseButtonDown",
            "MouseButtonUp",
            "UserEvent"
        ]:
            func = getattr(self, "ev_%s" % (event_type.lower(),))
            return func(event)

    def ev_quit(self, event: pg.QUIT) -> Optional[T]:
        """Called when the termination of the program is requested."""

    def ev_keydown(self, event: KEYDOWN) -> Optional[T]:
        pass

    def ev_keyup(self, event: KEYUP) -> Optional[T]:
        pass

    def ev_mousemotion(self, event) -> Optional[T]:
        pass

    def ev_mousebuttondown(self, event) -> Optional[T]:
        pass

    def ev_mousebuttonup(self, event) -> Optional[T]:
        pass

    def ev_mousewheel(self, event) -> Optional[T]:
        pass

    def ev_userevent(self, event) -> Optional[T]:
        pass

    def ev_(self, event: Any) -> Optional[T]:
        pass
