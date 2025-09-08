import tkinter as tk
from tkinter import colorchooser, ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")  # <-- doit être AVANT l'import de pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation

class ChartAnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Chart Tool (MVP)")
        self.setup_ui()
        self.default_settings()
        self.create_chart()

    def default_settings(self):
        self.chart_type = tk.StringVar(value="Line")
        self.speed = tk.DoubleVar(value=10.0)  # durée en secondes
        self.bg_color = "#ffffff"
        self.line_color = "#007ACC"
        self.bar_color = "#FF5733"
        self.axis_color = "#000000"
        self.anim = None

    def setup_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)

        # Chart type
        ttk.Label(frm, text="Chart Type:").grid(row=0, column=0, sticky="w")
        cmb = ttk.Combobox(frm, textvariable=self.chart_type,
                           values=["Line", "Bar"], state="readonly")
        cmb.grid(row=0, column=1, sticky="ew")
        cmb.bind("<<ComboboxSelected>>", lambda e: self.create_chart())

        # Animation duration
        ttk.Label(frm, text="Animation Duration (seconds):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.speed).grid(row=1, column=1, sticky="ew")

        # Color pickers
        ttk.Button(frm, text="Background Color", command=self.pick_bg_color).grid(row=2, column=0, sticky="ew")
        ttk.Button(frm, text="Line/Bar Color", command=self.pick_line_color).grid(row=2, column=1, sticky="ew")
        ttk.Button(frm, text="Axes Color", command=self.pick_axis_color).grid(row=2, column=2, sticky="ew")

        # Animate button
        ttk.Button(frm, text="Start Animation", command=self.animate_chart).grid(row=3, column=0, columnspan=3, pady=8)

        # Chart area
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, sticky="nsew")
        frm.rowconfigure(4, weight=1)
        frm.columnconfigure([0, 1, 2], weight=1)

    def pick_bg_color(self):
        color = colorchooser.askcolor(title="Background Color")[1]
        if color:
            self.bg_color = color

    def pick_line_color(self):
        color = colorchooser.askcolor(title="Line/Bar Color")[1]
        if color:
            if self.chart_type.get() == "Line":
                self.line_color = color
            else:
                self.bar_color = color

    def pick_axis_color(self):
        color = colorchooser.askcolor(title="Axes Color")[1]
        if color:
            self.axis_color = color

    def _style_axes(self):
        self.ax.set_facecolor(self.bg_color)
        for side in ("bottom", "left", "top", "right"):
            self.ax.spines[side].set_color(self.axis_color)
        self.ax.tick_params(axis='x', colors=self.axis_color)
        self.ax.tick_params(axis='y', colors=self.axis_color)

    def create_chart(self):
        # stop any running animation and clear
        if self.anim:
            self.anim.event_source.stop()
            self.anim = None

        self.ax.clear()
        x = np.linspace(0, 2*np.pi, 100)

        if self.chart_type.get() == "Line":
            self.lines = [self.ax.plot(x, np.sin(x), color=self.line_color, lw=2)[0]]
            self.bars = None
        else:
            self.bars = self.ax.bar(x[:10], np.abs(np.sin(x[:10])), color=self.bar_color)
            self.lines = None

        self._style_axes()
        self.canvas.draw_idle()

    def animate_chart(self):
        try:
            duration = float(self.speed.get())
        except Exception:
            messagebox.showerror("Invalid Input", "Duration must be a number.")
            return

        self.create_chart()
        frames = 100
        interval = int(max(10, duration * 1000 / frames))  # ms

        if self.chart_type.get() == "Line":
            x = np.linspace(0, 2*np.pi, 100)
            def update(frame):
                for i, line in enumerate(self.lines):
                    line.set_ydata(np.sin(x + frame / 10 + i))
                return self.lines
            self.anim = FuncAnimation(self.fig, update, frames=frames, interval=interval,
                                      blit=False, repeat=False)
        else:
            x = np.arange(10)
            def update(frame):
                for rect, val in zip(self.bars, np.abs(np.sin(x + frame / 10))):
                    rect.set_height(val)
                return self.bars
            self.anim = FuncAnimation(self.fig, update, frames=frames, interval=interval,
                                      blit=False, repeat=False)

        self.canvas.draw_idle()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChartAnimationApp(root)
    root.mainloop()
