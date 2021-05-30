import math
from typing import *
from euclid import Vector2, Vector3
from pleiades.utils.constants import Units, Science
from pleiades.utils.game_math import GMath


class EllipseMath:

    @staticmethod
    def semi_major_axis(sgp: float, specific_energy: float) -> float:
        return sgp / (2 * specific_energy)

    @staticmethod
    def semi_major_axis_from_apses(apoapsis: float, periapsis: float) -> float:
        return (apoapsis + periapsis) / 2

    @staticmethod
    def semi_major_axis_from_linear_eccentricity(linear_eccentricity: float, eccentricity: float) -> float:
        return linear_eccentricity * eccentricity

    @staticmethod
    def semi_minor_axis(semi_major_axis: float, eccentricity: float) -> float:
        return semi_major_axis * math.sqrt(1 - eccentricity * eccentricity)

    @staticmethod
    def semi_minor_axis_from_apses(apoapsis: float, periapsis: float) -> float:
        return math.sqrt(abs(apoapsis) * abs(periapsis))

    @staticmethod
    def linear_eccentricity(apoapsis: float, semi_major_axis: float) -> float:
        return apoapsis - semi_major_axis

    @staticmethod
    def linear_eccentricity_from_eccentricity(semi_major_axis: float, eccentricity: float) -> float:
        return semi_major_axis * eccentricity

    @staticmethod
    def eccentricity(linear_eccentricity: float, semi_major_axis: float) -> float:
        return linear_eccentricity / semi_major_axis

    @staticmethod
    def apoapsis(eccentricity: float, semi_major_axis: float) -> float:
        return (1 + eccentricity) * semi_major_axis

    @staticmethod
    def periapsis(eccentricity: float, semi_major_axis: float) -> float:
        return (1 - eccentricity) * semi_major_axis

    @staticmethod
    def semi_latus_rectum(semi_major_axis: float, eccentricity: float) -> float:
        if eccentricity == 0:
            return semi_major_axis
        return semi_major_axis * (1 - eccentricity * eccentricity)

    @staticmethod
    def area_of_ellipse_sector(
            semi_major_axis: float,
            semi_minor_axis: float,
            first_angle: float,
            second_angle: float
        ) -> float:
        theta = second_angle - first_angle

        a = math.atan2(
            (semi_minor_axis - semi_major_axis) * math.sin(2 * second_angle),
            (semi_major_axis + semi_minor_axis + (semi_minor_axis - semi_major_axis) * math.cos(2 * second_angle))
        )

        b = math.atan2(
            (semi_minor_axis - semi_major_axis) * math.sin(2 * first_angle),
            (semi_major_axis + semi_minor_axis + (semi_minor_axis - semi_major_axis) * math.cos(2 * first_angle))
        )

        return semi_major_axis * semi_minor_axis / 2 * (theta - a + b)

