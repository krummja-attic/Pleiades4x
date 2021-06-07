from __future__ import annotations
from typing import TYPE_CHECKING

import pygame_gui as pgui

if TYPE_CHECKING:
    pass


class Layout:

    def __init__(self, client: Client) -> None:
        self.client = client
        self.elements = {}

    def initialize(self):
        raise NotImplementedError()

    def register(self, key: str, element: pgui.core.UIElement) -> None:
        self.elements[key] = element

    def remove(self, key: str) -> None:
        del self.elements[key]
