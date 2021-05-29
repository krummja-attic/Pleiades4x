from ecstremity import Component, Entity
import math


class MassVolume(Component):

    def __init__(
            self,
            mass: float,
            volume: float,
        ) -> None:
        self._mass = mass
        self._volume = volume

    @property
    def mass_dry(self) -> float:
        """Mass in KG of this entity"""
        return self._mass

    @property
    def volume_km3(self) -> float:
        """Volume of this entity in KM^3"""
        return self._volume

    @property
    def volume_m3(self):
        return self._volume * 1e9

    @property
    def density_gcm(self):
        return

    @staticmethod
    def calculate_volume_km3(radius_au: float) -> float:
        return (4.0 / 3.0) * math.pi * math.pow(radius_au, 3)
