#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WordClock — Widget de escritorio para Windows.
Muestra la hora en palabras con la clásica matriz de letras iluminadas.

Uso en Windows:
    python wordclock.py
  o renómbralo a wordclock.pyw (o ejecútalo con pythonw) para que no
  aparezca la ventana de consola.

Controles:
    - Arrastra el widget con el botón izquierdo para moverlo.
    - Clic derecho: menú (opacidad, siempre visible, tamaño, tema, salir).
"""

import tkinter as tk
from datetime import datetime

# ---------------------------------------------------------------------------
# Matriz de letras (11 x 10) y posición de cada palabra: (fila, col_ini, col_fin)
# ---------------------------------------------------------------------------
GRID = [
    "ITLISASAMPM",
    "ACQUARTERDC",
    "TWENTYFIVEX",
    "HALFBTENFTO",
    "PASTERUNINE",
    "ONESIXTHREE",
    "FOURFIVETWO",
    "EIGHTELEVEN",
    "SEVENTWELVE",
    "TENSEOCLOCK",
]

WORDS = {
    "IT":      [(0, 0, 1)],
    "IS":      [(0, 3, 4)],
    "A":       [(1, 0, 0)],
    "QUARTER": [(1, 2, 8)],
    "TWENTY":  [(2, 0, 5)],
    "FIVE_M":  [(2, 6, 9)],   # "five" de minutos
    "HALF":    [(3, 0, 3)],
    "TEN_M":   [(3, 5, 7)],   # "ten" de minutos
    "TO":      [(3, 9, 10)],
    "PAST":    [(4, 0, 3)],
    "NINE":    [(4, 7, 10)],
    "ONE":     [(5, 0, 2)],
    "SIX":     [(5, 3, 5)],
    "THREE":   [(5, 6, 10)],
    "FOUR":    [(6, 0, 3)],
    "FIVE":    [(6, 4, 7)],
    "TWO":     [(6, 8, 10)],
    "EIGHT":   [(7, 0, 4)],
    "ELEVEN":  [(7, 6, 10)],
    "SEVEN":   [(8, 0, 4)],
    "TWELVE":  [(8, 5, 10)],
    "TEN":     [(9, 0, 2)],
    "OCLOCK":  [(9, 5, 10)],
}

HOURS = ["TWELVE", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX",
         "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN"]


def words_for_time(hour, minute):
    """Devuelve el conjunto de palabras a iluminar para una hora dada."""
    m = (minute // 5) * 5            # bloques de 5 minutos
    h = hour % 12
    words = {"IT", "IS"}

    if m == 0:
        words |= {HOURS[h], "OCLOCK"}
    elif m == 5:
        words |= {"FIVE_M", "PAST", HOURS[h]}
    elif m == 10:
        words |= {"TEN_M", "PAST", HOURS[h]}
    elif m == 15:
        words |= {"A", "QUARTER", "PAST", HOURS[h]}
    elif m == 20:
        words |= {"TWENTY", "PAST", HOURS[h]}
    elif m == 25:
        words |= {"TWENTY", "FIVE_M", "PAST", HOURS[h]}
    elif m == 30:
        words |= {"HALF", "PAST", HOURS[h]}
    elif m == 35:
        words |= {"TWENTY", "FIVE_M", "TO", HOURS[(h + 1) % 12]}
    elif m == 40:
        words |= {"TWENTY", "TO", HOURS[(h + 1) % 12]}
    elif m == 45:
        words |= {"A", "QUARTER", "TO", HOURS[(h + 1) % 12]}
    elif m == 50:
        words |= {"TEN_M", "TO", HOURS[(h + 1) % 12]}
    elif m == 55:
        words |= {"FIVE_M", "TO", HOURS[(h + 1) % 12]}
    return words


def lit_cells(words):
    """Convierte un conjunto de palabras en celdas (fila, col) iluminadas."""
    cells = set()
    for w in words:
        for row, c0, c1 in WORDS[w]:
            for c in range(c0, c1 + 1):
                cells.add((row, c))
    return cells


# ---------------------------------------------------------------------------
# Widget
# ---------------------------------------------------------------------------
THEMES = {
    "Oscuro": {"bg": "#111111", "off": "#2b2b2b", "on": "#f5f5f5",
               "dot_off": "#2b2b2b", "dot_on": "#ffb300"},
    "Claro":  {"bg": "#f2f2f2", "off": "#d9d9d9", "on": "#1a1a1a",
               "dot_off": "#d9d9d9", "dot_on": "#e65100"},
}

FONTS = ["Consolas", "Courier New", "monospace"]


class WordClockWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WordClock")
        self.root.overrideredirect(True)          # sin bordes ni barra de título
        self.root.attributes("-topmost", True)    # siempre visible
        self.root.attributes("-alpha", 0.95)

        self.theme_name = "Oscuro"
        self.font_size = 20
        self._drag = {}

        self._build_ui()
        self._build_menu()
        self._tick()

        # Posición inicial: esquina superior derecha
        self.root.update_idletasks()
        x = self.root.winfo_screenwidth() - self.root.winfo_width() - 40
        self.root.geometry(f"+{x}+40")

    # -- construcción ------------------------------------------------------
    def _build_ui(self):
        th = THEMES[self.theme_name]
        self.root.configure(bg=th["bg"])
        self.frame = tk.Frame(self.root, bg=th["bg"], padx=12, pady=12)
        self.frame.pack()

        self.cells = {}
        for r, row in enumerate(GRID):
            for c, ch in enumerate(row):
                lbl = tk.Label(self.frame, text=ch, bg=th["bg"], fg=th["off"],
                               font=(FONTS, self.font_size, "bold"),
                               padx=2, pady=1)
                lbl.grid(row=r + 1, column=c + 1)
                self.cells[(r, c)] = lbl

        # 4 puntos de minutos en las esquinas (minutos 1-4 extra)
        self.dots = []
        for (r, c) in [(0, 0), (0, 12), (11, 0), (11, 12)]:
            d = tk.Label(self.frame, text="●", bg=th["bg"], fg=th["dot_off"],
                         font=(FONTS, max(8, self.font_size // 2)))
            d.grid(row=r, column=c)
            self.dots.append(d)

        for w in (self.root, self.frame, *self.cells.values(), *self.dots):
            w.bind("<Button-1>", self._drag_start)
            w.bind("<B1-Motion>", self._drag_move)
            w.bind("<Button-3>", self._show_menu)

    def _build_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)
        op = tk.Menu(self.menu, tearoff=0)
        for label, alpha in [("100%", 1.0), ("85%", 0.85), ("70%", 0.70)]:
            op.add_command(label=label,
                           command=lambda a=alpha: self.root.attributes("-alpha", a))
        self.menu.add_cascade(label="Opacidad", menu=op)

        self.menu.add_command(label="Siempre visible: sí", command=self._toggle_topmost)

        sz = tk.Menu(self.menu, tearoff=0)
        sz.add_command(label="Más grande", command=lambda: self._resize(2))
        sz.add_command(label="Más pequeño", command=lambda: self._resize(-2))
        self.menu.add_cascade(label="Tamaño", menu=sz)

        tm = tk.Menu(self.menu, tearoff=0)
        for name in THEMES:
            tm.add_command(label=name, command=lambda n=name: self._set_theme(n))
        self.menu.add_cascade(label="Tema", menu=tm)

        self.menu.add_separator()
        self.menu.add_command(label="Salir", command=self.root.destroy)

    # -- comportamiento ----------------------------------------------------
    def _drag_start(self, event):
        self._drag = {"x": event.x_root - self.root.winfo_x(),
                      "y": event.y_root - self.root.winfo_y()}

    def _drag_move(self, event):
        self.root.geometry(f"+{event.x_root - self._drag['x']}"
                           f"+{event.y_root - self._drag['y']}")

    def _show_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def _toggle_topmost(self):
        cur = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not cur)
        self.menu.entryconfig(1, label=f"Siempre visible: {'sí' if not cur else 'no'}")

    def _resize(self, delta):
        self.font_size = max(10, min(40, self.font_size + delta))
        for lbl in self.cells.values():
            lbl.config(font=(FONTS, self.font_size, "bold"))

    def _set_theme(self, name):
        self.theme_name = name
        th = THEMES[name]
        self.root.configure(bg=th["bg"])
        self.frame.configure(bg=th["bg"])
        for lbl in self.cells.values():
            lbl.configure(bg=th["bg"])
        for d in self.dots:
            d.configure(bg=th["bg"], fg=th["dot_off"])
        self._paint(force=True)

    # -- reloj --------------------------------------------------------------
    def _paint(self, force=False):
        now = datetime.now()
        words = words_for_time(now.hour, now.minute)
        lit = lit_cells(words)
        th = THEMES[self.theme_name]
        sig = (frozenset(lit), now.minute % 5, self.theme_name)
        if not force and sig == getattr(self, "_last_sig", None):
            return
        self._last_sig = sig
        for (r, c), lbl in self.cells.items():
            lbl.config(fg=th["on"] if (r, c) in lit else th["off"])
        extra = now.minute % 5
        for i, d in enumerate(self.dots):
            d.config(fg=th["dot_on"] if i < extra else th["dot_off"])

    def _tick(self):
        self._paint()
        self.root.after(1000, self._tick)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    WordClockWidget().run()
