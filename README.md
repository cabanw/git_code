🌐 **WordClock**

WordClock is a lightweight world clock web application built with Python (Flask) and a modern HTML/CSS/JavaScript frontend.
It displays real-time clocks for multiple cities/time zones using Python’s built-in zoneinfo module.

Perfect for:

Remote teams

Global operations

Personal productivity dashboards

Learning Flask + frontend integration

✨ **Features**

⏰ Real-time clocks (updates every second)

🌍 Multiple time zones

🧩 Card-style clock widgets

🎨 Modern, responsive UI

⚡ Lightweight Flask backend

🕒 Accurate DST handling (zoneinfo)

💻**Runs locally in any modern browser**


🛠️ Tech Stack

Backend: Python 3.9+, Flask
🌍 **Supported Time Zones (Default)**

US East (New York)

US Central (Chicago)

US West (Los Angeles)

Puerto Rico

Spain (Madrid)

**You can add or remove cities easily in WordClock.py.**
🔧 Customization
Add a New City

Edit the cities dictionary in WordClock.py:

cities = {
    "Japan": "Asia/Tokyo",
    "UK": "Europe/London"
}

🔐 **Development Notes**

This uses Flask’s development server

Not intended for production without a WSGI server (e.g. Gunicorn, uWSGI)

Debug mode can be disabled in production
Frontend: HTML, CSS, JavaScript

Time Zones: zoneinfo (IANA Time Zone Database)

🚧 **Future Enhancements**

⏳ 12h / 24h toggle

🕰️ Analog clock widgets

➕ UI-based city selector

🖥 Desktop widget (.exe)

🌙 Dark/light theme toggle

💾 Save user preferences
