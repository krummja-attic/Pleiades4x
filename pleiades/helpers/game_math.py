import math
from typing import *


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
    pass


class Distance:
    pass


class PercentValue:
    pass


class WeightedValue:
    pass


class WeightedList:
    pass


class GMath:
    pass


class Intercept:
    pass



