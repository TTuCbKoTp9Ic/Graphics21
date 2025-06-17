# config.py

from series_builders import FSeriesBuilder, SinSeriesBuilder, FileSeriesBuilder, ISeriesBuilder
from typing import Dict

class Config:
    # Назви серій
    SIN_SERIES_NAME: str = "sin(x) (загальна)"
    F_SERIES_NAME: str = "F(x) (індивідуальна)"
    FILE_SERIES_NAME: str = "Функція з файлу"

    # Мапування до будівельників
    SERIES_BUILDERS: Dict[str, ISeriesBuilder] = {
        F_SERIES_NAME: FSeriesBuilder(),
        SIN_SERIES_NAME: SinSeriesBuilder(),
        FILE_SERIES_NAME: FileSeriesBuilder()
    }

    # Мапування до чекбоксів (ключі будуть іменами змінних у GUI)
    CHECKBOX_MAPPINGS: Dict[str, str] = {
        "sin_series_checkbox_var": SIN_SERIES_NAME,
        "individual_series_checkbox_var": F_SERIES_NAME,
        "file_series_checkbox_var": FILE_SERIES_NAME
    }

    # Типи графіка
    CHART_TYPE_DOT: str = "Точки"
    CHART_TYPE_LINE: str = "Лінія"

    # Мапування до стилів
    CHART_STYLE_MAPPINGS: Dict[str, str] = {
        CHART_TYPE_DOT: "o",
        CHART_TYPE_LINE: "-",
    }