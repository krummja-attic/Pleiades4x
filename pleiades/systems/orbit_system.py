from __future__ import annotations
from typing import *
from euclid import Vector3
import math

from dataclasses import dataclass

from pleiades.systems import BaseSystem

if TYPE_CHECKING:
    from ecstremity import Entity
    from pleiades.client import Client


class OrbitSystem(BaseSystem):

    accuracy_tolerance: float = 1e-6
    max_iterations: int = 5

    def initialize(self):
        self.query(key = "bodies", all_of = ["KeplerElements"])

    def update(self, time: float):
        bodies = self._queries["bodies"].result

        for body in bodies:
            _body = body["KeplerElements"]
            _body.compute_semi_constants()
            _body.mean_anomaly = _body.n * (time - _body.mean_longitude)

            E1 = _body.mean_anomaly
            for i in range(self.max_iterations):
                E0: float = E1
                E1 = (E0 - self.f(E0, _body.eccentricity, _body.mean_anomaly)
                      / self.derivative_f(E0, _body.eccentricity))

            _body.eccentric_anomaly = E1
            _body.true_anomaly = 2 * math.atan(_body.true_anomaly_constant * math.tan(_body.eccentric_anomaly / 2))

            distance: float = _body.semi_major_axis * (1 - _body.eccentricity * math.cos(_body.eccentric_anomaly))
            cosAOPPlusTA: float = math.cos(_body.argument_of_periapsis + _body.true_anomaly)
            sinAOPPlusTA: float = math.sin(_body.argument_of_periapsis + _body.true_anomaly)

            x: float = distance * (_body.cosLOAN * cosAOPPlusTA - _body.sinLOAN * sinAOPPlusTA * _body.cosI)
            y: float = distance * (_body.sinLOAN * cosAOPPlusTA - _body.cosLOAN * sinAOPPlusTA * _body.cosI)
            z: float = distance * (_body.sinI * sinAOPPlusTA)

            body["Position"].position = Vector3(x, y, z) + _body.parent["Position"].position

    @staticmethod
    def f(E: float, e: float, M: float) -> float:
        return M - E + e * math.sin(E)

    @staticmethod
    def derivative_f(E: float, e: float) -> float:
        return -1.0 + e * math.cos(E)
