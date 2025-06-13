# helpers/input_helper.py

import tkinter as tk
from tkinter import messagebox
from typing import Tuple, Optional # Додано для типу підказки

class InputHelper:
    @staticmethod
    def parse_input(input_str: str, field_name: str) -> Tuple[bool, Optional[float]]:
        """
        Парсить вхідний рядок у число з плаваючою комою та перевіряє його валідність.
        Виводить повідомлення про помилку, якщо ввід не валідний.
        """
        if not input_str.strip():
            messagebox.showerror("Помилка вводу", f"Поле '{field_name}' не може бути порожнім.")
            return False, None
        try:
            result = float(input_str)
            return True, result
        except ValueError:
            messagebox.showerror("Помилка вводу", f"Поле '{field_name}' містить недійсний ввід. Будь ласка, введіть дійсне число.")
            return False, None