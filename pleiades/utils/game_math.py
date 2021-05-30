import math
from typing import *
from euclid import Vector2, Vector3
from pleiades.utils.constants import Units, Science

T = TypeVar("T")


class Angle:

    @staticmethod
    def to_radians(degrees: float) -> float:
        """Convert degrees to radians"""
        return degrees * math.pi / 180

    @staticmethod
    def to_degrees(radians: float) -> float:
        """Convert radians to degrees"""
        return radians * 180 / math.pi

    @staticmethod
    def normalize_radians(radians: float) -> float:
        """Returns a number between -2pi and 2pi"""
        radians = radians % (2 * math.pi)
        return radians

    @staticmethod
    def normalize_radians_positive(radians: float) -> float:
        """Returns a number between 0 and 2pi"""
        radians = Angle.normalize_radians(radians)
        if radians < 0:
            radians += (2 * math.pi)
        return radians

    @staticmethod
    def normalize_degrees(degrees: float) -> float:
        """Returns a number between -360 and 360"""
        degrees = degrees % 360
        return degrees

    @staticmethod
    def difference_between_radians(a1: float, a2: float) -> float:
        return math.pi - abs(abs(a1 - a2) - math.pi)

    @staticmethod
    def difference_between_degrees(a1: float, a2: float) -> float:
        return 180 - abs(abs(a1 - a2) - 180)


class Temperature:

    @staticmethod
    def to_kelvin(celsius: float) -> float:
        return celsius + Units.celsius_to_kelvin

    @staticmethod
    def to_celsius(kelvin: float) -> float:
        return kelvin + Units.kelvin_to_celsius


class Distance:

    @staticmethod
    def meters_to_au(meters: Union[float, Vector3]) -> Union[float, Vector3]:
        if isinstance(meters, Vector3):
            return meters / (Units.meters_per_au, Units.meters_per_au, Units.meters_per_au)
        elif isinstance(meters, float):
            return meters / Units.meters_per_au
        else:
            raise TypeError(f"Must pass in a Vector3 or a float. Got {type(meters)}")

    @staticmethod
    def meters_to_kilometers(meters: float) -> float:
        return meters / 1000.0

    @staticmethod
    def kilometers_to_meters(kilometers: float) -> float:
        return kilometers * 1000.0

    @staticmethod
    def kilometers_to_au(kilometers: Union[float, Vector2, Vector3]) -> Union[float, Vector2, Vector3]:
        if isinstance(kilometers, Vector3):
            return Vector3(
                Distance.kilometers_to_au(kilometers.x),
                Distance.kilometers_to_au(kilometers.y),
                Distance.kilometers_to_au(kilometers.z),
            )
        elif isinstance(kilometers, Vector2):
            return Vector2(
                Distance.kilometers_to_au(kilometers.x),
                Distance.kilometers_to_au(kilometers.y),
            )
        elif isinstance(kilometers, float):
            return kilometers / Units.km_per_au
        else:
            raise TypeError(f"Must pass in a float, Vector2, or Vector3 - got {type(kilometers)}")

    @staticmethod
    def au_to_kilometers(au: Union[float, Vector2, Vector3]) -> Union[float, Vector2, Vector3]:
        if isinstance(au, Vector3):
            return Vector3(
                Distance.au_to_kilometers(au.x),
                Distance.au_to_kilometers(au.y),
                Distance.au_to_kilometers(au.z),
            )
        elif isinstance(au, Vector2):
            return Vector2(
                Distance.au_to_kilometers(au.x),
                Distance.au_to_kilometers(au.y),
            )
        elif isinstance(au, float):
            return au * Units.km_per_au
        else:
            raise TypeError(f"Must pass in a float, Vector2, or Vector3 - got {type(au)}")

    @staticmethod
    def au_to_meters(au: Union[float, Vector2, Vector3]) -> Union[float, Vector2, Vector3]:
        if isinstance(au, Vector3):
            return Vector3(
                Distance.au_to_meters(au.x),
                Distance.au_to_meters(au.y),
                Distance.au_to_meters(au.z),
            )
        elif isinstance(au, Vector2):
            return Vector2(
                Distance.au_to_meters(au.x),
                Distance.au_to_meters(au.y),
            )
        elif isinstance(au, float):
            return au * Units.meters_per_au
        else:
            raise TypeError(f"Must pass in a float, Vector2, or Vector3 - got {type(au)}")

    @staticmethod
    def between(p1: Vector3, p2: Vector3) -> Vector3:
        return p1 - p2


class GMath:

    @staticmethod
    def clamp(lower: float, val: float, upper: float) -> float:
        return min(max(lower, val), upper)

    @staticmethod
    def compute_gravitational_attraction(distance: float, mass1: float, mass2: float = 1) -> float:
        """Returns the gravitational attraction between two masses.

        Masses must be in kilograms. Distance between bodies must be in meters.
        Pass in only one mass to get the gravitational attraction of the given
        body at a specified distance.
        """
        return Science.gravitational_constant * mass1 * mass2 / (distance * distance)

    @staticmethod
    def compute_standard_gravitational_parameter(mass: float) -> float:
        return Science.gravitational_constant * mass

    @staticmethod
    def compute_standard_gravitational_parameter_km3s2(mass: float) -> float:
        return Science.gravitational_constant * mass / (1000 ** 3)

    @staticmethod
    def compute_standard_gravitational_parameter_au3s2(mass: float) -> float:
        return Science.gravitational_constant * mass / 3.347928976e33

    @staticmethod
    def get_vector(current: Vector3, target: Vector3, speed_mag_au: float) -> Vector3:
        length: float
        speed_mag_in_au = Vector3(0, 0, 0)
        direction = target - current
        length = math.sqrt(direction.x ** 2 + direction.y ** 2 + direction.z ** 2)

        if length != 0:
            direction = direction / length
            speed_mag_in_au = direction * speed_mag_au

        speed = speed_mag_in_au
        return speed


class Intercept:

    @staticmethod
    def hohmann_transfer(
            sgp: float,
            semi_maj_current: float,
            semi_maj_target: float,
        ) -> Tuple[Tuple[Vector3, float], Tuple[Vector3, float]]:
        transfer_orbit_semi_maj: float = semi_maj_current + semi_maj_target
        velocity_current_body: float = math.sqrt(sgp / semi_maj_current)
        velocity_target: float = math.sqrt(sgp / semi_maj_target)
        transfer_velocity_at_periapsis: float = math.sqrt(2 * (-sgp / transfer_orbit_semi_maj + sgp / semi_maj_current))
        transfer_velocity_at_apoapsis: float = math.sqrt(2 * (-sgp / transfer_orbit_semi_maj + sgp / semi_maj_target))

        delta_v_burn_1: float = transfer_velocity_at_periapsis - velocity_current_body
        delta_v_burn_2: float = transfer_velocity_at_apoapsis - velocity_target

        transfer_orbital_period: float = 2 * math.pi * math.sqrt(pow(transfer_orbit_semi_maj, 3) / sgp)
        time_to_second_burn: float = transfer_orbital_period * 0.5

        maneuvers = ((Vector3(0, delta_v_burn_1, 0), 0),
                     (Vector3(0, delta_v_burn_2, 0), time_to_second_burn))

        return maneuvers
