from __future__ import annotations
from typing import Tuple, Optional
from functools import cached_property

import numpy as np
import math
import scipy as sp
import scipy.constants as spc
from ecstremity import Component, Entity

from pleiades.utils.game_math import *
from pleiades.utils.constants import Units


class MassVolumeDB(Component):

    def __init__(self, mass: float, volume: float) -> None:
        """
        Database Component representing a body's mass in kilograms
        and volume in cubic kilometers.
        """
        self._mass = mass
        self._volume = volume

    @cached_property
    def mass(self):
        """Mass in kilograms."""
        return self._mass

    @cached_property
    def mass_in_grams(self):
        """Mass in grams."""
        return self.mass / spc.gram

    @cached_property
    def volume(self):
        """Volume in cubic kilometers."""
        return self._volume

    @cached_property
    def volume_in_meters(self):
        """Volume in cubic meters."""
        return self.volume * 1e9

    @cached_property
    def density(self):
        """Density in grams per cubic centimeter."""
        density_in_m3 = self.mass / self.volume_in_meters
        return density_in_m3 * spc.gram

    @cached_property
    def radius(self):
        """Radius in meters."""
        radius = pow((3 * self.mass) / (4 * math.pi * (self.density * spc.gram)), 0.3333333333)
        return Distance.kilometers_to_meters(radius / 1000 / 100)
