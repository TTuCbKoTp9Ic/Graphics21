# chart_controller.py

import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np

from helpers import InputHelper
from config import Config

class ChartController:
    def __init__(self, ui):
        self.ui = ui
        self.file_path = None

    def build_chart(self):
        # Отримання даних з полів GUI через спеціальний метод
        gui_data = self.ui.get_gui_data()
        
        # 1. Валідація
        all_error_messages = []
        is_x_min_valid, x_min, err_x_min = InputHelper.parse_input(gui_data["x_min"], "Від (X)")
        is_x_max_valid, x_max, err_x_max = InputHelper.parse_input(gui_data["x_max"], "До (X)")
        is_step_valid, step, err_step = InputHelper.parse_input(gui_data["step"], "Крок")
        is_y_min_valid, y_min, err_y_min = InputHelper.parse_input(gui_data["y_min"], "Від (Y)")
        is_y_max_valid, y_max, err_y_max = InputHelper.parse_input(gui_data["y_max"], "До (Y)")

        if not is_x_min_valid: all_error_messages.append(err_x_min)
        if not is_x_max_valid: all_error_messages.append(err_x_max)
        if not is_step_valid: all_error_messages.append(err_step)
        if not is_y_min_valid: all_error_messages.append(err_y_min)
        if not is_y_max_valid: all_error_messages.append(err_y_max)
        
        if all_error_messages:
            messagebox.showerror("Помилка вводу", "\n".join(all_error_messages))
            return

        # 2. Коригування діапазонів
        if x_min > x_max:
            x_min, x_max = x_max, x_min
            self.ui.x_min_input.delete(0, tk.END); self.ui.x_min_input.insert(0, str(x_min))
            self.ui.x_max_input.delete(0, tk.END); self.ui.x_max_input.insert(0, str(x_max))

        if y_min > y_max:
            y_min, y_max = y_max, y_min
            self.ui.y_min_input.delete(0, tk.END); self.ui.y_min_input.insert(0, str(y_min))
            self.ui.y_max_input.delete(0, tk.END); self.ui.y_max_input.insert(0, str(y_max))
        
        # 3. Валідація логіки
        if step <= 0:
            all_error_messages.append("Крок має бути додатним числом.")
        if (x_max - x_min < step) and (x_max != x_min):
            all_error_messages.append("Крок перевищує різницю між 'До (X)' та 'Від (X)'.")

        if all_error_messages:
            messagebox.showerror("Помилка вводу", "\n".join(all_error_messages))
            return
            
        self._draw_series(x_min, x_max, step, y_min, y_max)

    def _draw_series(self, x_min, x_max, step, y_min, y_max):
        self.ui.clear_series()
        active_series_names = self.ui.get_active_series()
        if not active_series_names:
            self.ui.sin_series_checkbox_var.set(True)
            active_series_names.append(Config.SIN_SERIES_NAME)
            messagebox.showinfo("Серія не обрана", f"Жодна серія не була обрана. '{Config.SIN_SERIES_NAME}' встановлено за замовчуванням.")
        
        x_points = [x_min] if x_min == x_max else np.arange(x_min, x_max + step / 2, step).tolist()

        plot_style = Config.CHART_STYLE_MAPPINGS.get(self.ui.chart_type_combobox.get(), "-")
        self.ui.set_plot_limits(x_min, x_max, y_min, y_max)

        for series_name in active_series_names:
            if series_name == Config.FILE_SERIES_NAME:
                try:
                    file_points = self._parse_file()
                    x_data = [p[0] for p in file_points]
                    y_data = [p[1] for p in file_points]
                    self.ui.plot_series(x_data, y_data, plot_style, series_name)
                except ValueError as e:
                    messagebox.showerror("Помилка файлу", str(e))
                    self.ui.file_series_checkbox_var.set(False)
                continue
            
            builder = Config.SERIES_BUILDERS.get(series_name)
            if builder:
                points = builder.build(x_points, y_min, y_max)
                valid_x = [p.x for p in points if not np.isnan(p.y)]
                valid_y = [p.y for p in points if not np.isnan(p.y)]
                self.ui.plot_series(valid_x, valid_y, plot_style, series_name)
        
        self.ui.update_chart(legend_needed=True)

    def apply_stretching(self):
        gui_data = self.ui.get_gui_data()
        is_coeff_valid, coeff, err = InputHelper.parse_input(gui_data["stretch_coeff"], "Коефіцієнт (Стиснення/Розтягування)")
        if not is_coeff_valid or coeff == 0:
            messagebox.showerror("Помилка", err or "Коефіцієнт не може бути нулем.")
            return

        for line in self.ui.ax.get_lines():
            x, y = line.get_data()
            if gui_data["stretch_axis"] == "Вісь X": line.set_xdata(np.array(x) * coeff)
            else: line.set_ydata(np.array(y) * coeff)
        self.ui.autoscale_chart()
        self.ui.update_chart(legend_needed=True)

    def apply_translation(self):
        gui_data = self.ui.get_gui_data()
        is_dx_valid, dx, err_dx = InputHelper.parse_input(gui_data["dx"], "Зсув по X")
        is_dy_valid, dy, err_dy = InputHelper.parse_input(gui_data["dy"], "Зсув по Y")
        if not is_dx_valid or not is_dy_valid:
            messagebox.showerror("Помилка", err_dx or err_dy)
            return

        for line in self.ui.ax.get_lines():
            x, y = line.get_data()
            line.set_xdata(np.array(x) + dx)
            line.set_ydata(np.array(y) + dy)
        self.ui.autoscale_chart()
        self.ui.update_chart(legend_needed=True)

    def apply_zoom(self):
        gui_data = self.ui.get_gui_data()
        is_coeff_valid, coeff, err = InputHelper.parse_input(gui_data["zoom_coeff"], "Коефіцієнт (Зум)")
        if not is_coeff_valid or coeff <= 0:
            messagebox.showerror("Помилка", err or "Коефіцієнт зуму має бути додатним.")
            return
            
        xlim, ylim = self.ui.ax.get_xlim(), self.ui.ax.get_ylim()
        new_w, new_h = (xlim[1] - xlim[0]) / coeff, (ylim[1] - ylim[0]) / coeff
        center_x, center_y = (xlim[0] + xlim[1]) / 2, (ylim[0] + ylim[1]) / 2
        self.ui.set_plot_limits(center_x - new_w / 2, center_x + new_w / 2, center_y - new_h / 2, center_y + new_h / 2)
        self.ui.update_chart()

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Оберіть текстовий файл", filetypes=(("Текстові файли", "*.txt"), ("Всі файли", "*.*")))
        if file_path:
            self.file_path = file_path
            self.ui.file_path_label.config(text=file_path.split('/')[-1], fg="black")
        else:
            self.file_path = None
            self.ui.file_path_label.config(text="Файл не обрано", fg="grey")

    def _parse_file(self) -> list[tuple[float, float]]:
        if not self.file_path: raise ValueError("Шлях до файлу не вказано.")
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) < 2: raise ValueError("Файл має містити щонайменше 2 рядки (X та Y).")
                x_str, y_str = lines[0].strip().split(), lines[1].strip().split()
                if len(x_str) != len(y_str): raise ValueError("Кількість точок X та Y не співпадає.")
                return list(zip([float(x) for x in x_str], [float(y) for y in y_str]))
        except Exception: raise ValueError("Неправильний формат даних у файлі.")