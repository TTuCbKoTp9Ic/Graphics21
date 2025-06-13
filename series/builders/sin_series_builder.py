# series/builders/sin_series_builder.py

import math
from typing import List, Optional
from models.series_point import SeriesPoint
from series.builders.i_series_builder import ISeriesBuilder

class SinSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]: 
        result = []
        for x in x_points:
            y = math.sin(x)
            result.append(SeriesPoint(x, y))
        return result