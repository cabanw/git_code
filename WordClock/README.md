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

## Despliegue — crear un .exe standalone

Para compartir el widget con alguien que no tiene Python instalado,
empaquétalo como ejecutable con PyInstaller:

1. Instala PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Desde la carpeta `WordClock`, genera el ejecutable:
   ```
   pyinstaller --onefile --noconsole --name WordClockES wordclock_widget_es.py
   ```
   - `--onefile`: crea un solo archivo .exe
   - `--noconsole`: no muestra la ventana de consola (equivale al `.pyw`)
   - `--name`: nombre del ejecutable final
   - Opcional: agrega `--icon=icono.ico` para usar un icono personalizado

3. El ejecutable queda en `dist/WordClockES.exe` (~20–30 MB). Es portable:
   cópialo a cualquier PC con Windows y funciona sin instalar nada.

Notas:
- La primera compilación tarda unos minutos.
- Algunos antivirus marcan los .exe generados por PyInstaller como
  sospechosos (falso positivo común); si ocurre, agrega una excepción.

### Arranque automático con Windows

1. Presiona `Win + R`, escribe `shell:startup` y Enter.
2. Crea un acceso directo a `WordClockES.exe` dentro de esa carpeta.

El widget arrancará solo al iniciar sesión.

## Versión web (original)

- `WordClock.py` + `templates/` — app Flask que muestra la hora actual en
  varias ciudades (US East, España, US Central, Puerto Rico, US West).

Uso:
```
pip install flask
python WordClock.py
```
