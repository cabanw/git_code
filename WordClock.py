import tkinter as tk
from datetime import datetime
import pytz

# Time zones
cities = {
    "US East": "America/New_York",
    "Spain": "Europe/Madrid",
    "US Central": "America/Chicago",
    "Puerto Rico": "America/Atlantic Standard Time",
    "US West": "America/Los_Angeles"
}

def update_time():
    text = ""
    for name, tz_name in cities.items():
        tz = pytz.timezone(tz_name)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        text += f"{name}: {current_time}\n"
    label.config(text=text)
    root.after(1000, update_time)  # update every second

root = tk.Tk()
root.title("🌐 World Clock")
root.attributes("-topmost", True)       # keep on top
root.attributes("-alpha", 0.85)         # transparency
root.overrideredirect(True)             # no window border

label = tk.Label(root, font=("Helvetica", 16), fg="white", bg="black", justify="left")
label.pack(padx=10, pady=10)

update_time()
root.mainloop()
