# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from chart_controller import ChartController
from config import Config

class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Приклад Графіків")
        self.geometry("950x850")
        self.resizable(True, True)

        self.legend = None
        self._create_widgets()
        # Створюємо контролер і передаємо йому посилання на себе (GUI)
        self.controller = ChartController(self)
        self._bind_events()

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
        
        self.file_series_checkbox_var = tk.BooleanVar(value=False)
        self.file_series_checkbox = ttk.Checkbutton(self.visualization_frame, text=Config.FILE_SERIES_NAME, variable=self.file_series_checkbox_var)
        self.file_series_checkbox.place(x=5, y=65)
        
        self.select_file_button = ttk.Button(self.visualization_frame, text="Обрати файл...")
        self.select_file_button.place(x=130, y=65, width=100)
        
        self.file_path_label = tk.Label(self.visualization_frame, text="Файл не обрано", font=("Arial", 7), fg="grey")
        self.file_path_label.place(x=10, y=95)
        
        tk.Label(self.visualization_frame, text="Тип графіка:").place(x=20, y=125)
        self.chart_type_combobox = ttk.Combobox(self.visualization_frame, values=[Config.CHART_TYPE_DOT, Config.CHART_TYPE_LINE], width=15, state="readonly")
        self.chart_type_combobox.set(Config.CHART_TYPE_LINE)
        self.chart_type_combobox.place(x=100, y=125)

        self.build_button = ttk.Button(self.visualization_frame, text="Побудувати")
        self.build_button.place(x=80, y=165, width=100)

        # Група "Стиснення / Розтягування"
        self.stretching_frame = ttk.LabelFrame(self, text="Стиснення / Розтягування")
        self.stretching_frame.place(x=670, y=470, width=260, height=120)

        tk.Label(self.stretching_frame, text="Вісь:").place(x=60, y=5)
        self.stretch_axis_combobox = ttk.Combobox(self.stretching_frame, values=["Вісь X", "Вісь Y"], width=15, state="readonly")
        self.stretch_axis_combobox.place(x=100, y=5)

        tk.Label(self.stretching_frame, text="Коефіцієнт:").place(x=15, y=35)
        self.stretch_coefficient_input = tk.Entry(self.stretching_frame, width=15)
        self.stretch_coefficient_input.insert(0, "1")
        self.stretch_coefficient_input.place(x=100, y=35)

        self.stretch_button = ttk.Button(self.stretching_frame, text="Застосувати")
        self.stretch_button.place(x=100, y=85)

        # Група "Паралельний перенос"
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

        self.translate_button = ttk.Button(self.translation_frame, text="Застосувати")
        self.translate_button.place(x=100, y=85)
        
        # Група "Масштабування (Зум)"
        self.zoom_frame = ttk.LabelFrame(self, text="Масштабування (Зум)")
        self.zoom_frame.place(x=670, y=730, width=260, height=90)

        tk.Label(self.zoom_frame, text="Коефіцієнт:").place(x=15, y=5)
        self.zoom_coefficient_input = tk.Entry(self.zoom_frame, width=15)
        self.zoom_coefficient_input.insert(0, "1")
        self.zoom_coefficient_input.place(x=100, y=5)

        self.zoom_button = ttk.Button(self.zoom_frame, text="Застосувати")
        self.zoom_button.place(x=100, y=45)

        self.canvas.draw()
    
    def _bind_events(self):
        """Прив'язує команди кнопок до методів контролера."""
        self.build_button.config(command=self.controller.build_chart)
        self.select_file_button.config(command=self.controller.select_file)
        self.stretch_button.config(command=self.controller.apply_stretching)
        self.translate_button.config(command=self.controller.apply_translation)
        self.zoom_button.config(command=self.controller.apply_zoom)

    # --- Методи для маніпуляції GUI, які викликає контролер ---

    def clear_series(self):
        self.ax.clear()
        self.ax.set_xlabel("Вісь X"); self.ax.set_ylabel("Вісь Y")
        self.ax.grid(True)
        self.ax.axhline(0, color='grey', linewidth=0.8)
        self.ax.axvline(0, color='grey', linewidth=0.8)
        self.autoscale_chart()
        if self.legend: self.legend.set_visible(False)

    def plot_series(self, x_data, y_data, style, label):
        if style == "o": # 'o' - це стиль для точок
            self.ax.plot(x_data, y_data, style, label=label, markersize=3)
        else:
            self.ax.plot(x_data, y_data, style, label=label)

    def set_plot_limits(self, x_min, x_max, y_min, y_max):
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
    
    def autoscale_chart(self):
        self.ax.relim()
        self.ax.autoscale_view()

    def update_chart(self, legend_needed=False):
        if legend_needed:
            lines_with_labels = [line for line in self.ax.get_lines() if not line.get_label().startswith('_')]
            if lines_with_labels:
                self.legend = self.ax.legend()
            elif self.legend:
                self.legend.set_visible(False)
        self.canvas.draw()

    def get_active_series(self):
        active_series = []
        for var_name, series_name in Config.CHECKBOX_MAPPINGS.items():
            if hasattr(self, var_name) and getattr(self, var_name).get():
                active_series.append(series_name)
        return active_series

    def get_gui_data(self):
        return {
            "x_min": self.x_min_input.get(), "x_max": self.x_max_input.get(),
            "y_min": self.y_min_input.get(), "y_max": self.y_max_input.get(),
            "step": self.step_input.get(),
            "stretch_coeff": self.stretch_coefficient_input.get(),
            "stretch_axis": self.stretch_axis_combobox.get(),
            "dx": self.dx_input.get(), "dy": self.dy_input.get(),
            "zoom_coeff": self.zoom_coefficient_input.get(),
            "chart_type": self.chart_type_combobox.get()
        }
    
    def _show_about(self):
        messagebox.showinfo("Про програму", "Ця програма візуалізує математичні функції.\nРозроблена для комп'ютерно-технологічної практики.")

    def _show_instructions(self):
        messagebox.showinfo("Інструкції", "Введіть діапазон для осей X та Y.\nОберіть потрібні функції, тип графіка та натисніть 'Побудувати'.\nТрансформації застосовуються до вже побудованих графіків.")