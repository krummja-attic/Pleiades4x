from __future__ import annotations
from typing import TYPE_CHECKING

from pleiades.states.state import State
from pleiades.renderer import Renderer
from pleiades.layouts import game

if TYPE_CHECKING:
    from pleiades.client import Client


class Game(State[None]):

    def __init__(self, client: Client):
        super().__init__(client)

    def on_enter(self):
        self.layout = game.Game(self.client)

    def draw(self, dt: float):
        pass

    def cmd_escape(self):
        self.client.pop_state()

    def ui_nav_up(self):
        print("UP")

    def ui_nav_left(self):
        print("LEFT")

    def ui_nav_down(self):
        print("DOWN")

    def ui_nav_right(self):
        print("RIGHT")

    def ui_zoom_in(self):
        print("IN")

    def ui_zoom_out(self):
        print("OUT")
