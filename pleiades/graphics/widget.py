from __future__ import annotations
from typing import Tuple, Optional
import pygame
from pleiades.graphics import constants


def unmask(widget: Widget) -> None:
    unmask_all(widget)
    widget.mask_children = True


def unmask_all(widget: Widget) -> None:
    widget.self_mask = True
    widget.do_mask = lambda: None


def call_on_change(data_member, callback, *args, **kwargs):
    """Creates a data member that calls a function when changed."""

    def get(self):
        return getattr(self, data_member)

    def set(self, my_value):
        if data_member in self.__dict__:
            change = (my_value != self.__dict__[data_member])
        else:
            change = True
        if change:
            setattr(self, data_member, my_value)
            callback(self, *args, **kwargs)

    return property(get, set)


def set_on_change(data_member, set_me, set_value: bool = True):
    return call_on_change(data_member, setattr, set_me, set_value)


def causes_rebuild(data_member):
    return set_on_change(data_member, "needs_rebuild")


def causes_redraw(data_member):
    return set_on_change(data_member, "needs_redraw")


def causes_resize(data_member):
    return set_on_change(data_member, "needs_resize")


def causes_reposition(data_member):
    return set_on_change(data_member, "needs_reposition")


def causes_update(data_member):
    return set_on_change(data_member, "needs_update")


def propagate_need(data_member):
    def do_propagate(self):
        if getattr(self, data_member, False):
            self.needs_update = True
            if hasattr(self, "children"):
                descendants = self.children[:]
                while descendants:
                    child = descendants.pop()
                    if not getattr(child, data_member, False):
                        setattr(child, data_member, True)
                        child._needs_update = True
                        if hasattr(child, "children"):
                            descendants += child.children
    return do_propagate


class auto_reconfigure:

    __slots__ = ["data_member", "reconfig_data_member", "reconfig_function"]

    def __init__(self, data_member, reconfig_prefix, reconfig_func):
        self.data_member = data_member
        self.reconfig_data_member = reconfig_prefix + data_member
        self.reconfig_function = reconfig_func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.data_member)

    def __set__(self, obj, value):
        new_value = self.reconfig_function(value)
        setattr(obj, self.reconfig_data_member, new_value)
        setattr(obj, self.data_member, value)

    def reconfigure(self, obj):
        updated_value = self.reconfig_function(getattr(obj, self.data_member))
        setattr(obj, self.reconfig_data_member, updated_value)


class Widget:

    needs_redraw = call_on_change("_needs_redraw", propagate_need("_needs_redraw"))
    needs_resize = call_on_change("_needs_resize", propagate_need("_needs_resize"))
    needs_reposition = call_on_change("_needs_reposition", propagate_need("_needs_reposition"))
    needs_rebuild = causes_update("_needs_rebuild")

    def _propagate_update(self):
        if self._needs_update:
            if hasattr(self, "parent"):
                target = self.parent
                while target and not target._needs_update:
                    target._needs_update = True
                    target = target.parent

    needs_update = call_on_change("_needs_update", _propagate_update)
    needs_reconfig = call_on_change("_needs_reconfig", propagate_need("_needs_reconfig"))

    pos = causes_reposition("_pos")
    size = causes_resize("_size")
    anchor = causes_reposition("_anchor")
    visible = causes_redraw("_visible")

    def __init__(
            self,
            parent: Optional[Widget],
            pos: Tuple[int, int],
            size: Tuple[int, int],
            anchor: Tuple[int, int] = constants.TOP_LEFT
        ) -> None:
        self._parent = parent
        self.children = []
        self._pos = pos
        self._size = size
        self._anchor = anchor

        self.add_hooks()

        self.is_above_mask = False
        self.self_mask = False
        self.mask_children = False
        self.visible = True

        self.needs_rebuild = True
        self.collision_rect = None
        self.needs_reconfig = True

    @property
    def parent(self) -> Optional[Widget]:
        if self._parent:
            return self._parent
        return None

    @parent.setter
    def parent(self, value: Widget) -> None:
        self._parent = value

    def add_hooks(self):
        if self.parent:
            for child in self.children:
                child.add_hooks()

    def remove_hooks(self):
        children = self.children
        for child in children:
            child.remove_hooks()

    def _parent_size(self):
        pass

    def _calc_size(self):
        pass

    def get_real_size(self):
        pass

    @property
    def real_pos(self):
        return

    def make_collision_rect(self):
        pass

    def is_colliding(self):
        pass

    def remake_surfaces(self):
        pass

    def prepare_for_redraw(self):
        pass

    def maybe_update(self):
        pass

    def update(self):
        pass

    def _update(self):
        pass

    def reconfigure(self):
        pass

    def resize(self):
        pass

    def reposition(self):
        pass

    def redraw(self):
        pass

    def add_handler(self):
        pass

    def remove_handler(self):
        pass

    def add_key_handler(self):
        pass

    def remove_key_handler(self):
        pass

    def add_focus_widget(self):
        pass

    def remove_focus_widget(self):
        pass

    def took_focus(self):
        pass

    def clear_focus(self):
        pass
