# config.py

from series.builders.random_series_builder import RandomSeriesBuilder
from series.builders.F_series_builder import FSeriesBuilder
from series.builders.sin_series_builder import SinSeriesBuilder
from series.builders.file_series_builder import FileSeriesBuilder # <<< ДОДАНО ЦЕЙ ІМПОРТ
from typing import Dict
from series.builders.i_series_builder import ISeriesBuilder

class Config:
    # Назви серій, які будуть відображатися в легенді та коді
    SIN_SERIES_NAME: str = "sin(x) (загальна)"
    F_SERIES_NAME: str = "F(x) (індивідуальна)"
    RANDOM_SERIES_NAME: str = "Випадкові числа"
    FILE_SERIES_NAME: str = "Функція з файлу"

    # Мапування назв серій до їхніх будівельників
    SERIES_BUILDERS: Dict[str, ISeriesBuilder] = {
        RANDOM_SERIES_NAME: RandomSeriesBuilder(),
        F_SERIES_NAME: FSeriesBuilder(),
        SIN_SERIES_NAME: SinSeriesBuilder(),
        FILE_SERIES_NAME: FileSeriesBuilder()
    }

    # Мапування назв чекбоксів до відповідних назв серій
    CHECKBOX_MAPPINGS: Dict[str, str] = {
        "sin_series_checkbox": SIN_SERIES_NAME,
        "individual_series_checkbox": F_SERIES_NAME,
        "random_series_checkbox": RANDOM_SERIES_NAME,
        "file_series_checkbox": FILE_SERIES_NAME
    }

    # Додаткові константи для типу графіка
    CHART_TYPE_DOT: str = "Точки"
    CHART_TYPE_LINE: str = "Лінія"

    # Мапування назв до стилів matplotlib
    CHART_STYLE_MAPPINGS: Dict[str, str] = {
        CHART_TYPE_DOT: "o", # Колові маркери
        CHART_TYPE_LINE: "-", # Суцільна лінія
    }