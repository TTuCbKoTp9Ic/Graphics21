# series/builders/random_series_builder.py

import random
from typing import List, Optional
from models.series_point import SeriesPoint
from series.builders.i_series_builder import ISeriesBuilder
import tkinter.messagebox as messagebox

class RandomSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        if y_min is None or y_max is None:
            # Це повідомлення, ймовірно, не буде викликано, якщо логіка main_form коректна.
            # Але залишаємо для надійності.
            messagebox.showerror("Помилка", "Неможливо побудувати випадкову серію. Будь ласка, встановіть діапазон для осі Y.")
            raise ValueError("Діапазон для генерації випадкових чисел не встановлено.")

        result = []
        for x in x_points:
            y = random.uniform(y_min, y_max) # Використовуємо y_min, y_max
            result.append(SeriesPoint(x, y))
        return result