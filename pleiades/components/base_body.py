from __future__ import annotations
from typing import Optional, List, Union

from ecstremity import Component, Entity


class BaseBody(Component):

    def __init__(self) -> None:
        self._parent: Optional[str] = None
        self._children: List[str] = []

    @property
    def parent(self) -> str:
        return self._parent

    @parent.setter
    def parent(self, value: Union[str, Entity]) -> None:
        if isinstance(value, Entity):
            value = entity.uid
        self._parent = value

    def add_child(self, new_child: Union[str, Entity]) -> None:
        if isinstance(entity_or_uid, Entity):
            new_child = entity_or_uid.uid
        self._children.append(new_child)

    def add_children(self, new_children: List[Union[str, Entity]]) -> None:
        for child in new_children:
            self.add_child(child)
