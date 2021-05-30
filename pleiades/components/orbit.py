from __future__ import annotations
from typing import Tuple, Optional
from functools import cached_property
from dataclasses import dataclass
import datetime

import numpy as np
import math
import scipy as sp
import scipy.constants as spc
from ecstremity import Component, Entity

from pleiades.utils.game_math import *
from pleiades.utils.constants import Units


class OrbitDB(Component):

    def __init__(self, velocity, date_time) -> None:
        """
        Database Component representing a body's orbital properties.
        Velocity is in meters per second.
        """
        self.velocity = velocity
        self.date_time = date_time

    @property
    def semi_major_axis(self):
        """Semi-Major Axis in meters."""
        return

    @property
    def semi_major_axis_au(self):
        """Semi-Major Axis in Astronomical Units."""
        return

    @property
    def eccentricity(self):
        return

    @property
    def inclination_degrees(self):
        return

    @property
    def longitude_of_ascending_node(self):
        return

    @property
    def longitude_of_ascending_node_degrees(self):
        return

    @property
    def argument_of_periapsis(self):
        return

    @property
    def argument_of_periapsis_degrees(self):
        return

    @property
    def mean_anomaly_at_epoch(self):
        return

    @property
    def mean_anomaly_at_epoch_degrees(self):
        return

    @property
    def gravitational_parameter_m3s2(self):
        return

    @property
    def gravitational_parameter_km3s2(self):
        return

    @property
    def orbital_period(self):
        return

    @property
    def mean_motion_deg_sec(self):
        return

    @property
    def apoapsis(self):
        return

    @property
    def apoapsis_au(self):
        return

    @property
    def periapsis(self):
        return

    @property
    def periapsis_au(self):
        return

    @property
    def parent_mass(self):
        return

    @property
    def mass(self):
        return
