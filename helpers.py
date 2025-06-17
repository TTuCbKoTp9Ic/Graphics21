# helpers.py

import tkinter as tk
from typing import Tuple, Optional

class InputHelper:
    @staticmethod
    def parse_input(input_str: str, field_name: str) -> Tuple[bool, Optional[float], Optional[str]]:
        if not input_str.strip():
            return False, None, f"Поле '{field_name}' не може бути порожнім."
        try:
            result = float(input_str)
            return True, result, None
        except ValueError:
            return False, None, f"Поле '{field_name}' містить недійсний ввід. Будь ласка, введіть дійсне число."