# forms/main_form.py

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
from typing import List, Optional

from helpers.input_helper import InputHelper
from config import Config

class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Приклад Графіків")
        self.geometry("950x850") # Збільшена висота для нових елементів
        self.resizable(True, True)

        self.file_path: Optional[str] = None
        self.legend = None  # Атрибут для зберігання об'єкта легенди

        self._create_widgets()

    def _create_widgets(self):
        # Меню-бар
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Довідка", menu=help_menu)
        help_menu.add_command(label="Про програму", command=self._show_about)
        help_menu.add_command(label="Інструкції", command=self._show_instructions)

        # Область для графіка
        self.fig = Figure(figsize=(6.5, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Вісь X")
        self.ax.set_ylabel("Вісь Y")
        self.ax.grid(True)
        self.ax.axhline(0, color='grey', linewidth=0.8)
        self.ax.axvline(0, color='grey', linewidth=0.8)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.place(x=10, y=30, width=650, height=610)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        toolbar.place(x=10, y=640)

        # Група "Діапазон X"
        self.x_range_frame = ttk.LabelFrame(self, text="Діапазон X")
        self.x_range_frame.place(x=670, y=30, width=260, height=120)
        tk.Label(self.x_range_frame, text="Від:").place(x=50, y=5)
        self.x_min_input = tk.Entry(self.x_range_frame, width=15)
        self.x_min_input.insert(0, "-1")
        self.x_min_input.place(x=100, y=5)
        tk.Label(self.x_range_frame, text="До:").place(x=50, y=35)
        self.x_max_input = tk.Entry(self.x_range_frame, width=15)
        self.x_max_input.insert(0, "1")
        self.x_max_input.place(x=100, y=35)
        tk.Label(self.x_range_frame, text="Крок:").place(x=40, y=65)
        self.step_input = tk.Entry(self.x_range_frame, width=15)
        self.step_input.insert(0, "0.1")
        self.step_input.place(x=100, y=65)

        # Група "Діапазон Y"
        self.y_range_frame = ttk.LabelFrame(self, text="Діапазон Y")
        self.y_range_frame.place(x=670, y=160, width=260, height=90)
        tk.Label(self.y_range_frame, text="Від:").place(x=50, y=5)
        self.y_min_input = tk.Entry(self.y_range_frame, width=15)
        self.y_min_input.insert(0, "-1")
        self.y_min_input.place(x=100, y=5)
        tk.Label(self.y_range_frame, text="До:").place(x=50, y=35)
        self.y_max_input = tk.Entry(self.y_range_frame, width=15)
        self.y_max_input.insert(0, "1")
        self.y_max_input.place(x=100, y=35)

        # Група "Візуалізація"
        self.visualization_frame = ttk.LabelFrame(self, text="Візуалізація")
        self.visualization_frame.place(x=670, y=260, width=260, height=200)
        self.sin_series_checkbox_var = tk.BooleanVar(value=True)
        self.sin_series_checkbox = ttk.Checkbutton(self.visualization_frame, text=Config.SIN_SERIES_NAME, variable=self.sin_series_checkbox_var)
        self.sin_series_checkbox.place(x=5, y=5)
        self.individual_series_checkbox_var = tk.BooleanVar(value=False)
        self.individual_series_checkbox = ttk.Checkbutton(self.visualization_frame, text=Config.F_SERIES_NAME, variable=self.individual_series_checkbox_var)
        self.individual_series_checkbox.place(x=5, y=35)
        self.random_series_checkbox_var = tk.BooleanVar(value=False)
        self.random_series_checkbox = ttk.Checkbutton(self.visualization_frame, text=Config.RANDOM_SERIES_NAME, variable=self.random_series_checkbox_var)
        self.random_series_checkbox.place(x=5, y=65)
        self.file_series_checkbox_var = tk.BooleanVar(value=False)
        self.file_series_checkbox = ttk.Checkbutton(self.visualization_frame, text=Config.FILE_SERIES_NAME, variable=self.file_series_checkbox_var)
        self.file_series_checkbox.place(x=5, y=95)
        self.select_file_button = ttk.Button(self.visualization_frame, text="Обрати файл...", command=self._select_file)
        self.select_file_button.place(x=130, y=95, width=100)
        self.file_path_label = tk.Label(self.visualization_frame, text="Файл не обрано", font=("Arial", 7), fg="grey")
        self.file_path_label.place(x=10, y=125)
        tk.Label(self.visualization_frame, text="Тип графіка:").place(x=20, y=155)
        self.chart_type_combobox = ttk.Combobox(self.visualization_frame, values=[Config.CHART_TYPE_DOT, Config.CHART_TYPE_LINE], width=15, state="readonly")
        self.chart_type_combobox.set(Config.CHART_TYPE_LINE)
        self.chart_type_combobox.place(x=100, y=155)

        # Група "Стиснення / Розтягування" (змінює дані)
        self.stretching_frame = ttk.LabelFrame(self, text="Стиснення / Розтягування")
        self.stretching_frame.place(x=670, y=470, width=260, height=120)

        tk.Label(self.stretching_frame, text="Вісь:").place(x=60, y=5)
        self.stretch_axis_combobox = ttk.Combobox(self.stretching_frame, values=["Вісь X", "Вісь Y"], width=15, state="readonly")
        self.stretch_axis_combobox.place(x=100, y=5)

        tk.Label(self.stretching_frame, text="Коефіцієнт:").place(x=15, y=35)
        self.stretch_coefficient_input = tk.Entry(self.stretching_frame, width=15)
        self.stretch_coefficient_input.place(x=100, y=35)

        self.stretch_button = ttk.Button(self.stretching_frame, text="Застосувати", command=self._apply_stretching)
        self.stretch_button.place(x=100, y=85)

        # Група "Паралельний перенос" (змінює дані)
        self.translation_frame = ttk.LabelFrame(self, text="Паралельний перенос")
        self.translation_frame.place(x=670, y=600, width=260, height=120)

        tk.Label(self.translation_frame, text="Зсув по X:").place(x=20, y=5)
        self.dx_input = tk.Entry(self.translation_frame, width=15)
        self.dx_input.insert(0, "0")
        self.dx_input.place(x=100, y=5)

        tk.Label(self.translation_frame, text="Зсув по Y:").place(x=20, y=35)
        self.dy_input = tk.Entry(self.translation_frame, width=15)
        self.dy_input.insert(0, "0")
        self.dy_input.place(x=100, y=35)

        self.translate_button = ttk.Button(self.translation_frame, text="Застосувати", command=self._apply_translation)
        self.translate_button.place(x=100, y=85)
        
        # Нова група "Масштабування (Зум)" (змінює вигляд)
        self.zoom_frame = ttk.LabelFrame(self, text="Масштабування (Зум)")
        self.zoom_frame.place(x=670, y=730, width=260, height=90) # Нове розміщення

        tk.Label(self.zoom_frame, text="Коефіцієнт:").place(x=15, y=5)
        self.zoom_coefficient_input = tk.Entry(self.zoom_frame, width=15)
        self.zoom_coefficient_input.insert(0, "1") # Значення за замовчуванням
        self.zoom_coefficient_input.place(x=100, y=5)

        self.zoom_button = ttk.Button(self.zoom_frame, text="Застосувати", command=self._apply_zoom)
        self.zoom_button.place(x=100, y=45)


        # Кнопки "Побудувати" та "Скинути"
        self.build_button = ttk.Button(self, text="Побудувати", command=self._build_chart)
        self.build_button.place(x=740, y=820, width=80) # Оновлене розміщення

        self.reset_button = ttk.Button(self, text="Скинути", command=self._clear_series)
        self.reset_button.place(x=830, y=820, width=80) # Оновлене розміщення

        self.canvas.draw()
    
    def _select_file(self):
        """Відкриває діалог вибору файлу та зберігає шлях."""
        file_path = filedialog.askopenfilename(
            title="Оберіть текстовий файл",
            filetypes=(("Текстові файли", "*.txt"), ("Всі файли", "*.*"))
        )
        if file_path:
            self.file_path = file_path
            file_name = file_path.split('/')[-1]
            self.file_path_label.config(text=file_name, fg="black")
        else:
            self.file_path = None
            self.file_path_label.config(text="Файл не обрано", fg="grey")

    def _parse_file(self) -> List[tuple[float, float]]:
        """Читає та парсить файл з точками."""
        if not self.file_path:
            raise ValueError("Шлях до файлу не вказано.")
        
        try:
            with open(self.file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) < 2:
                    raise ValueError("Файл має містити щонайменше 2 рядки (для X та Y).")

                x_values_str = lines[0].strip().split()
                y_values_str = lines[1].strip().split()

                if len(x_values_str) != len(y_values_str):
                    raise ValueError("Кількість точок X та Y у файлі не співпадає.")
                
                x_values = [float(x) for x in x_values_str]
                y_values = [float(y) for y in y_values_str]

                return list(zip(x_values, y_values))
        except FileNotFoundError:
            raise ValueError(f"Файл не знайдено за шляхом: {self.file_path}")
        except (ValueError, IndexError):
            raise ValueError("Неправильний формат даних у файлі. Очікується два рядки з числами, розділеними пробілами.")
    
    def _show_about(self):
        messagebox.showinfo("Про програму", "Ця програма візуалізує математичні функції.\nРозроблена для комп'ютерно-технологічної практики.")

    def _show_instructions(self):
        messagebox.showinfo("Інструкції", "Введіть діапазон для осей X та Y.\nОберіть потрібні функції, тип графіка та натисніть 'Побудувати'.\nТрансформації застосовуються до вже побудованих графіків.")

    def _build_chart(self):
        is_x_min_valid, x_min = InputHelper.parse_input(self.x_min_input.get(), "Від (X)")
        is_x_max_valid, x_max = InputHelper.parse_input(self.x_max_input.get(), "До (X)")
        is_step_valid, step = InputHelper.parse_input(self.step_input.get(), "Крок")
        if not (is_x_min_valid and is_x_max_valid and is_step_valid):
            messagebox.showerror("Помилка", "Перевірте введені дані для діапазону X.")
            return
        if step <= 0:
            messagebox.showerror("Помилка", "Крок має бути додатним числом.")
            return
        is_y_min_valid, y_min = InputHelper.parse_input(self.y_min_input.get(), "Від (Y)")
        is_y_max_valid, y_max = InputHelper.parse_input(self.y_max_input.get(), "До (Y)")
        if not (is_y_min_valid and is_y_max_valid):
            messagebox.showerror("Помилка", "Перевірте введені дані для діапазону Y.")
            return
        if x_min > x_max:
            messagebox.showinfo("Діапазон X змінено", "'Від' більше за 'До'. Значення поміняні місцями.")
            x_min, x_max = x_max, x_min
            self.x_min_input.delete(0, tk.END); self.x_min_input.insert(0, str(x_min))
            self.x_max_input.delete(0, tk.END); self.x_max_input.insert(0, str(x_max))
        if y_min > y_max:
            messagebox.showinfo("Діапазон Y змінено", "'Від' більше за 'До'. Значення поміняні місцями.")
            y_min, y_max = y_max, y_min
            self.y_min_input.delete(0, tk.END); self.y_min_input.insert(0, str(y_min))
            self.y_max_input.delete(0, tk.END); self.y_max_input.insert(0, str(y_max))
        self._draw_series(x_min, x_max, step, y_min, y_max)

    def _draw_series(self, x_min: float, x_max: float, step: float, y_min: float, y_max: float):
        self._clear_series()
        active_series_names = self._get_active_series()
        if not active_series_names:
            self.sin_series_checkbox_var.set(True)
            active_series_names.append(Config.SIN_SERIES_NAME)
            messagebox.showinfo("Серія не обрана", f"Жодна серія не була обрана. '{Config.SIN_SERIES_NAME}' встановлено за замовчуванням.")
        
        x_points = np.arange(x_min, x_max + step/2, step).tolist()
        if not x_points:
            messagebox.showerror("Помилка", "Для заданого діапазону X та кроку не згенеровано жодної точки.")
            return

        selected_chart_type = self.chart_type_combobox.get()
        plot_style = Config.CHART_STYLE_MAPPINGS.get(selected_chart_type, "-")
        
        # Переконаємося, що початкові межі осей встановлюються відповідно до введених Y
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_xlim(x_min, x_max)

        for series_name in active_series_names:
            if series_name == Config.FILE_SERIES_NAME:
                try:
                    file_points = self._parse_file()
                    valid_x = [p[0] for p in file_points]
                    valid_y = [p[1] for p in file_points]
                    self.ax.plot(valid_x, valid_y, plot_style, label=series_name)
                except ValueError as e:
                    messagebox.showerror("Помилка файлу", str(e))
                    self.file_series_checkbox_var.set(False)
                continue
            
            builder = Config.SERIES_BUILDERS.get(series_name)
            if builder:
                try:
                    points = builder.build(x_points, y_min, y_max)
                    valid_x = [p.x for p in points if not np.isnan(p.y)]
                    valid_y = [p.y for p in points if not np.isnan(p.y)]
                    if selected_chart_type == Config.CHART_TYPE_DOT:
                        self.ax.plot(valid_x, valid_y, plot_style, label=series_name, markersize=3)
                    else:
                        self.ax.plot(valid_x, valid_y, plot_style, label=series_name)
                except ValueError as e:
                    messagebox.showerror("Помилка серії", f"Помилка при побудові серії '{series_name}': {e}")
                    if series_name == Config.RANDOM_SERIES_NAME: self.random_series_checkbox_var.set(False)
                    elif series_name == Config.F_SERIES_NAME: self.individual_series_checkbox_var.set(False)
                    elif series_name == Config.SIN_SERIES_NAME: self.sin_series_checkbox_var.set(False)
                    continue

        lines_with_labels = [line for line in self.ax.get_lines() if not line.get_label().startswith('_')]
        if lines_with_labels:
            self.legend = self.ax.legend()
        elif self.legend:
            self.legend.set_visible(False)
        self.canvas.draw()

    def _clear_series(self):
        self.ax.clear()
        self.ax.set_xlabel("Вісь X"); self.ax.set_ylabel("Вісь Y")
        self.ax.grid(True)
        self.ax.axhline(0, color='grey', linewidth=0.8)
        self.ax.axvline(0, color='grey', linewidth=0.8)
        self.ax.autoscale_view(True, True, True)
        if self.legend:
            self.legend.set_visible(False)
        self.canvas.draw()

    def _get_active_series(self) -> List[str]:
        active_series = []
        if self.sin_series_checkbox_var.get(): active_series.append(Config.SIN_SERIES_NAME)
        if self.individual_series_checkbox_var.get(): active_series.append(Config.F_SERIES_NAME)
        if self.random_series_checkbox_var.get(): active_series.append(Config.RANDOM_SERIES_NAME)
        if self.file_series_checkbox_var.get(): active_series.append(Config.FILE_SERIES_NAME)
        return active_series

    def _apply_stretching(self):
        """Застосовує стиснення/розтягування до існуючих графіків через зміну даних."""
        axis_selection = self.stretch_axis_combobox.get()
        is_coeff_valid, coefficient = InputHelper.parse_input(self.stretch_coefficient_input.get(), "Коефіцієнт")
        if not is_coeff_valid or coefficient == 0:
            messagebox.showerror("Помилка", "Коефіцієнт має бути дійсним числом і не дорівнювати нулю.")
            return
        if not axis_selection:
            messagebox.showerror("Помилка", "Будь ласка, оберіть вісь для трансформації.")
            return
        lines = self.ax.get_lines()
        if not lines:
            messagebox.showinfo("Інформація", "Немає графіків для трансформації.")
            return
        
        for line in lines:
            x_data, y_data = line.get_data()
            x_data_np = np.array(x_data)
            y_data_np = np.array(y_data)

            if axis_selection == "Вісь X":
                line.set_xdata(x_data_np * coefficient)
            elif axis_selection == "Вісь Y":
                line.set_ydata(y_data_np * coefficient)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
    
    def _apply_translation(self):
        """Застосовує паралельний перенос до існуючих графіків через зміну даних."""
        is_dx_valid, dx = InputHelper.parse_input(self.dx_input.get(), "Зсув по X")
        is_dy_valid, dy = InputHelper.parse_input(self.dy_input.get(), "Зсув по Y")
        if not (is_dx_valid and is_dy_valid):
            messagebox.showerror("Помилка", "Значення зсуву мають бути дійсними числами.")
            return
        lines = self.ax.get_lines()
        if not lines:
            messagebox.showinfo("Інформація", "Немає графіків для переносу.")
            return
        
        for line in lines:
            x_data, y_data = line.get_data()
            x_data_np = np.array(x_data)
            y_data_np = np.array(y_data)

            line.set_xdata(x_data_np + dx)
            line.set_ydata(y_data_np + dy)
        
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
    
    def _apply_zoom(self):
        """Застосовує масштабування (зум) до вигляду графіка, змінюючи межі осей."""
        is_coeff_valid, coefficient = InputHelper.parse_input(self.zoom_coefficient_input.get(), "Коефіцієнт")
        if not is_coeff_valid or coefficient <= 0:
            messagebox.showerror("Помилка", "Коефіцієнт має бути додатним дійсним числом.")
            return
        
        # Щоб зум не впливав на поточні графіки, ми не перевіряємо наявність ліній.
        # Зум завжди змінює вигляд, незалежно від наявності даних.

        # Отримуємо поточні межі
        current_xlim = self.ax.get_xlim()
        current_ylim = self.ax.get_ylim()

        # Знаходимо центр видимої області
        center_x = (current_xlim[0] + current_xlim[1]) / 2
        center_y = (current_ylim[0] + current_ylim[1]) / 2

        # Знаходимо поточну ширину та висоту видимої області
        width = current_xlim[1] - current_xlim[0]
        height = current_ylim[1] - current_ylim[0]
        
        # Обчислюємо нову ширину та висоту.
        # Коефіцієнт > 1 -> приближення (зум-ін), ширина/висота зменшуються.
        # Коефіцієнт < 1 -> віддалення (зум-аут), ширина/висота збільшуються.
        new_width = width / coefficient
        new_height = height / coefficient
        
        # Встановлюємо нові межі відносно центру
        self.ax.set_xlim(center_x - new_width / 2, center_x + new_width / 2)
        self.ax.set_ylim(center_y - new_height / 2, center_y + new_height / 2)
        
        self.canvas.draw()