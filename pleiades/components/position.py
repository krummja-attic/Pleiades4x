from __future__ import annotations
from typing import Tuple, Optional
from functools import cached_property

import numpy as np
import math
import scipy as sp
import scipy.constants as spc

from euclid import Vector3
from ecstremity import Component, Entity

from pleiades.utils.game_math import *
from pleiades.utils.constants import Units


class Position(Component):

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            z: int = 0,
            system_uid: str = "<unset>"
        ) -> None:
        """Database Component representing a body's spatial position.

        Absolute position is a Vector3 in kilometers.
        """
        self._position = Vector3(x, y, z)
        self.system_uid = system_uid

    @property
    def position(self) -> Vector3:
        return self._position

    @position.setter
    def position(self, value: Vector3) -> None:
        self._position = value

    @property
    def xy(self):
        return self.position.x, self.position.y

    @property
    def parent(self):
        if self.entity["BASEBODY"].has_parent:
            return self.entity["BASEBODY"].parent
        return None

    @cached_property
    def position_meters(self):
        position_m = Vector3(
            self.position.x * 0.001,
            self.position.y * 0.001,
            self.position.z * 0.001,
        )
        return position_m

    @cached_property
    def position_au(self):
        position_au = Vector3(
            self.position.x / Units.km_per_au,
            self.position.y / Units.km_per_au,
            self.position.z / Units.km_per_au
        )
        return position_au

    @cached_property
    def relative_position_meters(self):
        if self.parent:
            parent_pos: Vector3 = self.parent["POSITIONDB"].position_meters
            relative_pos_m = Vector3(
                parent_pos.x - self.position_meters.x,
                parent_pos.y - self.position_meters.y,
                parent_pos.z - self.position_meters.z,
            )
            return relative_pos_m
        return None

    @cached_property
    def relative_position_au(self):
        if self.parent:
            parent_pos: Vector3 = self.parent["POSITIONDB"].position_au
            relative_pos_au = Vector3(
                parent_pos.x - self.position_au.x,
                parent_pos.y - self.position_au.y,
                parent_pos.z - self.position_au.z,
            )
            return relative_pos_au
        return None
