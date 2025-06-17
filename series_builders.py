# series_builders.py

import math
import numpy as np
from typing import List, Optional
from abc import ABC, abstractmethod

# Клас SeriesPoint
class SeriesPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Інтерфейс ISeriesBuilder
class ISeriesBuilder(ABC):
    @abstractmethod
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        pass

# Будівельник для Sin(x)
class SinSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        result = []
        for x in x_points:
            y = math.sin(x)
            result.append(SeriesPoint(x, y))
        return result

# Допоміжна функція для F(x)
def _real_cbrt(x):
    if x >= 0:
        return x**(1/3)
    else:
        return -(-x)**(1/3)

# Будівельник для F(x)
class FSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        result = []
        for x in x_points:
            y = np.nan
            try:
                if 7 < x < 9:
                    arg1 = x**3 / 7
                    if math.tan(arg1) == 0: raise ValueError()
                    term1 = 2 * (1 / math.tan(arg1))
                    arg2_abs = 1.3**2 + x**3
                    if arg2_abs <= 0: raise ValueError()
                    term2 = math.exp(x) * math.log(abs(arg2_abs))
                    if (3 - x) == 0: raise ValueError()
                    term3 = (6 * x) / (3 - x)
                    y = term1 - term2 + term3
                elif -5 < x < -3:
                    y = _real_cbrt(x) + 3
                else:
                    if x == 0: raise ValueError()
                    y = x**(-2) + 1
            except (ValueError, OverflowError):
                y = np.nan
            result.append(SeriesPoint(x, y))
        return result

# Фіктивний будівельник для файлової серії
class FileSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        return []