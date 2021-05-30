from __future__ import annotations
from typing import *
import math
from euclid import Vector3


def length(vector: Vector3) -> float:
    return math.sqrt(length_squared(vector))


def length_squared(vector: Vector3) -> float:
    return (vector.x * vector.x) + (vector.y * vector.y)
