from ecstremity import Component
from pleiades.utils.constants import Units


class Mass(Component):

    def __init__(self, value: float = 100.0) -> None:
        self.value = value
