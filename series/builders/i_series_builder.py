# series/builders/i_series_builder.py

from abc import ABC, abstractmethod
from typing import List, Optional
from models.series_point import SeriesPoint

class ISeriesBuilder(ABC):
    """
    Інтерфейс для будівельників серій графіків.
    """
    @abstractmethod
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        """
        Будує список точок для серії графіка на основі заданих точок X.
        y_min та y_max використовуються для генерації випадкових значень Y.
        """
        pass