from typing import *
from dataclasses import dataclass
from euclid import Vector2, Vector3
import math
from datetime import date

from sys import float_info

from pleiades.utils.classproperty import classproperty
from pleiades.utils.constants import Units, Science
from pleiades.utils.game_math import *
from pleiades.utils.ellipse_math import EllipseMath
from pleiades.utils import vector3 as vectools


@dataclass
class KeplerElements:
    semi_major_axis: float
    semi_minor_axis: float
    eccentricity: float
    periapsis: float
    apoapsis: float
    longitude_of_ascending_node: float
    argument_of_periapsis: float
    inclination: float
    mean_motion: float
    mean_anomaly_at_epoch: float
    true_anomaly_at_epoch: float
    orbital_period: float
    epoch: date

    @property
    def linear_eccentricity_from_eccentricity(self):
        return self.eccentricity * self.semi_major_axis

    @property
    def linear_eccentricity_from_apoapsis(self):
        return EllipseMath.linear_eccentricity(self.apoapsis, self.semi_major_axis)


class OrbitMath:

    @classproperty
    def epsilon(self) -> float:
        return 1e-15

    @staticmethod
    def kepler_from_position_and_velocity(
            sgp: float,
            position: Vector3,
            velocity: Vector3,
            epoch: date = date.today()
        ) -> KeplerElements:
        angular_velocity: Vector3 = position.cross(velocity)
        node_vector: Vector3 = Vector3(0, 0, 1).cross(angular_velocity)
        eccentricity_vector: Vector3 = OrbitMath.eccentricity_vector(sgp, position, velocity)
        eccentricity: float = vectools.length(eccentricity_vector)
        specific_orbital_energy: float = pow(vectools.length(velocity), 2) * 0.5 - sgp / vectools.length(position)
        semi_major_axis: float

        if abs(eccentricity) > 1:  # hyperbola
            semi_major_axis = -(-sgp / (2 * specific_orbital_energy))
        elif abs(eccentricity) < 1:  # ellipse
            semi_major_axis = -sgp / (2 * specific_orbital_energy)
        else:  # parabola
            semi_major_axis = float_info.max

        semi_minor_axis: float = EllipseMath.semi_minor_axis(semi_major_axis, eccentricity)

        try:
            inclination: float = math.acos(angular_velocity.z / vectools.length(angular_velocity))
        except ZeroDivisionError:
            inclination = 0

        longitude_of_ascending_node: float = OrbitMath.calculate_longitude_of_ascending_node(node_vector)
        true_anomaly: float = OrbitMath.calculate_true_anomaly(eccentricity_vector, position, velocity)
        argument_of_periapsis: float = OrbitMath.calculate_argument_of_periapsis(
            position,
            inclination,
            longitude_of_ascending_node,
            true_anomaly
        )

        mean_motion = math.sqrt(sgp / pow(semi_major_axis, 3))

        eccentric_anomaly: float = OrbitMath.calculate_eccentric_anomaly_from_true_anomaly(true_anomaly, eccentricity)

        mean_anomaly: float = OrbitMath.calculate_mean_anomaly(eccentricity, eccentric_anomaly)

        return KeplerElements(
            semi_major_axis = semi_major_axis,
            semi_minor_axis = semi_minor_axis,
            eccentricity = eccentricity,
            periapsis = EllipseMath.periapsis(eccentricity, semi_major_axis),
            apoapsis = EllipseMath.apoapsis(eccentricity, semi_major_axis),
            longitude_of_ascending_node = longitude_of_ascending_node,
            argument_of_periapsis = argument_of_periapsis,
            inclination = inclination,
            mean_motion = mean_motion,
            mean_anomaly_at_epoch = mean_anomaly,
            true_anomaly_at_epoch = true_anomaly,
            orbital_period = 2 * math.pi * math.sqrt(pow(semi_major_axis, 3) / sgp),
            epoch = epoch
        )

    @staticmethod
    def eccentricity_vector(sgp: float, position: Vector3, velocity: Vector3) -> Vector3:
        angular_momentum: Vector3 = position.cross(velocity)
        a: Vector3 = velocity.cross(angular_momentum) / sgp
        b: Vector3 = position / vectools.length(position)
        E: Vector3 = a - b
        if vectools.length(E) < OrbitMath.epsilon:
            return Vector3(0, 0, 0)
        return E

    @staticmethod
    def calculate_longitude_of_ascending_node(node_vector: Vector3) -> float:
        try:
            length = node_vector.x / vectools.length(node_vector)
        except ZeroDivisionError:
            length = 0

        length = GMath.clamp(-1, length, 1)
        longitude_of_ascending_node: float = 0.0

        if length != 0:
            longitude_of_ascending_node = math.acos(length)
        return longitude_of_ascending_node

    @staticmethod
    def calculate_true_anomaly(
            eccentricity_vector: Vector3,
            position: Vector3,
            velocity: Vector3
        ) -> float:
        e = vectools.length(eccentricity_vector)
        r = vectools.length(position)

        if e > OrbitMath.epsilon:  # circular orbit
            dot_ecc_pos: Vector3 = eccentricity_vector.dot(position)
            talen: float = e * r
            talen = dot_ecc_pos / talen
            talen = GMath.clamp(-1, talen, 1)
            true_anomaly: float = math.acos(talen)
            if position.dot(velocity) < 0:
                true_anomaly = math.pi * 2 - true_anomaly
            return Angle.normalize_radians_positive(true_anomaly)
        else:
            return Angle.normalize_radians_positive(math.atan2(position.y, position.x))  # circular, assume AoP is 0

    @staticmethod
    def calculate_argument_of_periapsis(
            position: Vector3,
            inclination: float,
            longitude_of_ascending_node: float,
            true_anomaly: float
        ) -> float:
        Sw: float
        Rx: float = position.x
        Ry: float = position.y
        Rz: float = position.z
        R: float = vectools.length(position)
        TA: float = true_anomaly
        Cw = (Rx * math.cos(longitude_of_ascending_node) + Ry * math.sin(longitude_of_ascending_node) / R)

        if inclination == 0 or inclination == math.pi:
            Sw = (Ry * math.cos(longitude_of_ascending_node) - Rx * math.sin(longitude_of_ascending_node) / R)
        else:
            Sw = Rz / (R * math.sin(inclination))

        W = math.atan2(Sw, Cw) - TA
        if W < 0:
            W = 2 * math.pi + W
        return W

    @staticmethod
    def calculate_eccentric_anomaly_from_true_anomaly(true_anomaly: float, eccentricity: float) -> float:
        E = math.acos((math.acos(true_anomaly) + eccentricity) / (1 + eccentricity * math.cos(true_anomaly)))
        if true_anomaly > math.pi or true_anomaly < 0 and true_anomaly > -math.pi:
            E = -E
        return E

    @staticmethod
    def calculate_mean_anomaly(eccentricity: float, eccentric_anomaly: float) -> float:
        return eccentric_anomaly - eccentricity * math.sin(eccentric_anomaly)
