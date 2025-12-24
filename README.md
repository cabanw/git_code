# 🌐 WordClock

**WordClock** is a lightweight world clock web application built with **Python (Flask)** and a modern **HTML/CSS/JavaScript** frontend.  
It displays real-time clocks for multiple cities and time zones using Python’s built-in **`zoneinfo`** module for accurate DST handling.

Ideal for:
- 🌍 Remote teams
- 🏢 Global operations
- 📊 Personal productivity dashboards
- 📚 Learning Flask + frontend integration

---

## ✨ Features

- ⏰ Real-time clocks (updates every second)
- 🌍 Multiple time zones
- 🧩 Card-style clock widgets
- 🎨 Modern, responsive UI
- ⚡ Lightweight Flask backend
- 🕒 Accurate DST handling via `zoneinfo`
- 💻 Runs locally in any modern browser

---

## 🛠️ Tech Stack

**Backend**
- Python 3.9+
- Flask

**Frontend**
- HTML
- CSS
- JavaScript

**Time Zones**
- `zoneinfo` (IANA Time Zone Database)

---

## 🌍 Supported Time Zones (Default)

- 🇺🇸 US East — New York
- 🇺🇸 US Central — Chicago
- 🇺🇸 US West — Los Angeles
- 🇵🇷 Puerto Rico
- 🇪🇸 Spain — Madrid

> You can easily add or remove cities in `WordClock.py`.

---

## 🔧 Customization

### ➕ Add a New City

Edit the `cities` dictionary in `WordClock.py`:

```python
cities = {
    "Japan": "Asia/Tokyo",
    "UK": "Europe/London"
}
