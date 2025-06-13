# series/builders/file_series_builder.py

from typing import List, Optional
from models.series_point import SeriesPoint
from series.builders.i_series_builder import ISeriesBuilder

class FileSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        return []