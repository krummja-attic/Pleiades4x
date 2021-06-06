from ecstremity import Component
import math

from pleiades.utils.constants import Science


class KeplerElements(Component):

    def __init__(
            self,
            semi_major_axis: float,
            eccentricity: float = 0.0,
            inclination: float = 0.0,
            swivel: float = 0.0,
            position: float = 0.0,
            offset: float = 0.0,
            anomaly: float = 0.0,
        ) -> None:
        self.semi_major_axis = semi_major_axis

        self.eccentricity = min(max(0.0, eccentricity), 0.99)
        self.inclination = min(max(0.0, inclination), Science.tau)

        self.longitude_of_ascending_node: float = min(max(0.0, swivel), Science.tau)
        self.argument_of_periapsis: float = min(max(0.0, position), Science.tau)
        self.mean_longitude: float = offset
        self.mean_anomaly: float = anomaly

        # Computed semi-constants
        self.mu: float = 0.0
        self.n: float = 0.0
        self.cosLOAN: float = 0.0
        self.sinLOAN: float = 0.0
        self.cosI: float = 0.0
        self.sinI: float = 0.0
        self.true_anomaly_constant: float = 0.0

    @property
    def parent(self):
        if self.entity["BASEBODY"].has_parent:
            return self.entity["BASEBODY"].parent_entity

    def compute_semi_constants(self):
        self.mu = Science.gravitational_constant * self.parent["Mass"].value
        self.n = math.sqrt(self.mu / pow(self.semi_major_axis, 3))
        self.true_anomaly_constant = math.sqrt((1 + self.eccentricity) / (1 - self.eccentricity))
        self.cosLOAN = math.cos(self.longitude_of_ascending_node)
        self.sinLOAN = math.sin(self.longitude_of_ascending_node)
        self.cosI = math.cos(self.inclination)
        self.sinI = math.sin(self.inclination)
