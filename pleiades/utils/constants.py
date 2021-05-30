from pleiades.utils.classproperty import classproperty


class Science:
    gravitational_constant: float = 6.67408e-11


class Units:
    solar_mass_in_kg: float = 1.98855e30
    earth_mass_in_kg: float = 5.97219e24
    sol_mass_in_earth_masses: int = 332946
    km_per_light_year: float = 9460730472580.8
    meters_per_au: int = 149597870700
    solar_radius_in_km: float = 696342.0
    earth_gravity: float = 9.81
    earth_radius_in_km: float = 6367.5
    earth_volume_in_km3: float = 1083206916846.0
    earth_atmosphere_in_kpa: float = 101.325
    celsius_to_kelvin: float = 273.15
    kelvin_to_celsius: float = -273.15

    @classproperty
    def au_per_light_year(self) -> float:
        return self.km_per_light_year / self.km_per_au

    @classproperty
    def km_per_au(self) -> float:
        return self.meters_per_au / 1000

    @classproperty
    def solar_radius_in_au(self) -> float:
        return self.solar_radius_in_km / self.km_per_au
