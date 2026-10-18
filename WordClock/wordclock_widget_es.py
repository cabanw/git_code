#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WordClock ES — Widget de escritorio para Windows, versión en español.
Muestra la hora en palabras con la clásica matriz de letras iluminadas.

Ejemplos de lo que verás encendido:
    SON LAS DOCE EN PUNTO
    ES LA UNA Y CUARTO
    SON LAS TRES Y MEDIA
    SON LAS DOS MENOS DIEZ

Uso en Windows:
    python wordclock_es.py
  o renómbralo a wordclock_es.pyw (o ejecútalo con pythonw) para que no
  aparezca la ventana de consola.

Controles:
    - Arrastra el widget con el botón izquierdo para moverlo.
    - Clic derecho: menú (opacidad, siempre visible, tamaño, tema, salir).
"""

import tkinter as tk
from datetime import datetime

# ---------------------------------------------------------------------------
# Matriz de letras (12 x 11) y posición de cada palabra: (fila, col_ini, col_fin)
# Se construye por programa para que las posiciones sean exactas.
# ---------------------------------------------------------------------------
COLS = 11
LAYOUT = [  # (palabra, fila, columna_inicial)
    ("ES", 0, 0), ("LAS", 0, 3), ("SON", 0, 7),
    ("LA", 1, 0), ("UNA", 1, 3), ("DOS", 1, 7),
    ("TRES", 2, 0), ("CUATRO", 2, 5),
    ("CINCO", 3, 0), ("SEIS", 3, 6),
    ("SIETE", 4, 0), ("OCHO", 4, 6),
    ("NUEVE", 5, 0), ("DIEZ", 5, 6),
    ("ONCE", 6, 0), ("DOCE", 6, 5), ("Y", 6, 10),
    ("CUARTO", 7, 0), ("MEDIA", 7, 6),
    ("VEINTE", 8, 0), ("MENOS", 8, 6),
    ("DIEZ_M", 9, 0), ("CINCO_M", 9, 5),
    ("VEINTICINCO", 10, 0),
    ("EN", 11, 0), ("PUNTO", 11, 3),
]

_FILLER = "AOEIURTN"  # letras de relleno (rotadas para no formar palabras)


def _build_grid():
    rows = max(r for _, r, _ in LAYOUT) + 1
    grid = [["" for _ in range(COLS)] for _ in range(rows)]
    words = {}
    for word, row, col0 in LAYOUT:
        cells = []
        letters = word.replace("_M", "")  # DIEZ_M / CINCO_M ocupan solo sus letras
        for i, ch in enumerate(letters):
            grid[row][col0 + i] = ch
            cells.append((row, col0 + i))
        words[word] = cells
    # Rellena los huecos con letras que no forman palabras reales.
    for r in range(rows):
        for c in range(COLS):
            if not grid[r][c]:
                grid[r][c] = _FILLER[(r * COLS + c) % len(_FILLER)]
    return ["".join(row) for row in grid], words


GRID, WORDS = _build_grid()

HOURS = ["DOCE", "UNA", "DOS", "TRES", "CUATRO", "CINCO", "SEIS",
         "SIETE", "OCHO", "NUEVE", "DIEZ", "ONCE"]


def _hour_phrase(h):
    """Devuelve las palabras de cabecera: ES LA UNA / SON LAS <hora>."""
    if h % 12 == 1:
        return {"ES", "LA", "UNA"}
    return {"SON", "LAS", HOURS[h % 12]}


def words_for_time(hour, minute):
    """Devuelve el conjunto de palabras a iluminar para una hora dada."""
    m = (minute // 5) * 5            # bloques de 5 minutos
    h = hour % 12
    words = set()

    if m == 0:
        words |= _hour_phrase(h) | {"EN", "PUNTO"}
    elif m == 5:
        words |= _hour_phrase(h) | {"Y", "CINCO_M"}
    elif m == 10:
        words |= _hour_phrase(h) | {"Y", "DIEZ_M"}
    elif m == 15:
        words |= _hour_phrase(h) | {"Y", "CUARTO"}
    elif m == 20:
        words |= _hour_phrase(h) | {"Y", "VEINTE"}
    elif m == 25:
        words |= _hour_phrase(h) | {"Y", "VEINTICINCO"}
    elif m == 30:
        words |= _hour_phrase(h) | {"Y", "MEDIA"}
    elif m == 35:
        words |= _hour_phrase((h + 1) % 12) | {"MENOS", "VEINTICINCO"}
    elif m == 40:
        words |= _hour_phrase((h + 1) % 12) | {"MENOS", "VEINTE"}
    elif m == 45:
        words |= _hour_phrase((h + 1) % 12) | {"MENOS", "CUARTO"}
    elif m == 50:
        words |= _hour_phrase((h + 1) % 12) | {"MENOS", "DIEZ_M"}
    elif m == 55:
        words |= _hour_phrase((h + 1) % 12) | {"MENOS", "CINCO_M"}
    return words


def lit_cells(words):
    """Convierte un conjunto de palabras en celdas (fila, col) iluminadas."""
    cells = set()
    for w in words:
        for row, col in WORDS[w]:
            cells.add((row, col))
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
        self.root.title("WordClock ES")
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
        rows, cols = len(GRID), len(GRID[0])
        self.dots = []
        for (r, c) in [(0, 0), (0, cols + 1), (rows + 1, 0), (rows + 1, cols + 1)]:
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
