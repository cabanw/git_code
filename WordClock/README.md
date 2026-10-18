# WordClock

Reloj de palabras en dos sabores.

## Widget de escritorio (nuevo)

- `wordclock_widget.py` — versión en inglés ("IT IS HALF PAST TEN")
- `wordclock_widget_es.py` — versión en español ("SON LAS TRES Y MEDIA")

Widget sin bordes para Windows, siempre visible, arrastrable, con menú de
clic derecho (opacidad, tamaño, tema claro/oscuro). Solo necesita Python
(tkinter viene incluido).

Uso:
```
python wordclock_widget_es.py
```
Tip: renómbralo a `.pyw` para que no aparezca la ventana de consola, y
pon un acceso directo en `shell:startup` para que arranque con Windows.

## Versión web (original)

- `WordClock.py` + `templates/` — app Flask que muestra la hora actual en
  varias ciudades (US East, España, US Central, Puerto Rico, US West).

Uso:
```
pip install flask
python WordClock.py
```
