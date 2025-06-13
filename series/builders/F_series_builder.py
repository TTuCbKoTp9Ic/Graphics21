# series/builders/F_series_builder.py

import math
from typing import List, Optional
from models.series_point import SeriesPoint
from series.builders.i_series_builder import ISeriesBuilder
import numpy as np

# Допоміжна функція для обчислення дійсного кубічного кореня
def real_cbrt(x):
    if x >= 0:
        return x**(1/3)
    else:
        return -(-x)**(1/3)

class FSeriesBuilder(ISeriesBuilder):
    def build(self, x_points: List[float], y_min: Optional[float] = None, y_max: Optional[float] = None) -> List[SeriesPoint]:
        result = []
        for x in x_points:
            y = np.nan

            try:
                if 7 < x < 9:
                    arg1 = x**3 / 7
                    if math.tan(arg1) == 0:
                        raise ValueError(f"ctg({arg1}) is undefined (tan({arg1}) is zero).")
                    term1 = 2 * (1 / math.tan(arg1))

                    arg2_abs = 1.3**2 + x**3
                    if arg2_abs <= 0:
                        raise ValueError(f"Logarithm argument ({arg2_abs}) must be positive.")
                    term2 = math.exp(x) * math.log(abs(arg2_abs))
                    
                    if (3 - x) == 0:
                        raise ValueError(f"Division by zero for (3 - x) when x=3.")
                    term3 = (6 * x) / (3 - x)
                    
                    y = term1 - term2 + term3

                elif -5 < x < -3:
                    # F(x) = x^(1/3) + 3 -- ВИПРАВЛЕНО ДЛЯ ВІД'ЄМНИХ ЧИСЕЛ
                    y = real_cbrt(x) + 3

                else:
                    if x == 0:
                        raise ValueError("Division by zero for x^-2 when x=0.")
                    y = x**(-2) + 1
                    
            except ValueError as e:
                y = np.nan
            except OverflowError:
                y = np.nan
            except Exception as e:
                y = np.nan
                
            result.append(SeriesPoint(x, y))
        return result