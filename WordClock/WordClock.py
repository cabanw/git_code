from flask import Flask, jsonify, render_template
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

cities = {
    "US East": "America/New_York",
    "Spain": "Europe/Madrid",
    "US Central": "America/Chicago",
    "Puerto Rico": "America/Puerto_Rico",
    "US West": "America/Los_Angeles"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/time")
def get_time():
    data = {}
    for name, tz_name in cities.items():
        tz = ZoneInfo(tz_name)
        data[name] = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
