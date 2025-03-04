from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_basicauth import BasicAuth
from prisma import Prisma
from prisma.models import Device, Measurement
from datetime import datetime

from auth import basic_auth, init_basic_auth
from routes.tts_uplink import tts_uplink_blueprint

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})  # Allow frontend requests

# ✅ Initialize Prisma but don't connect yet
db = Prisma()

# ✅ Connect to Prisma only once when the app starts
try:
    db.connect()
    print("✅ Prisma database connected successfully")
except Exception as e:
    print(f"❌ Failed to connect to Prisma database: {str(e)}")
    db = None  # Prevent using an uninitialized client

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """ Fetch all devices """
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        devices = db.device.find_many()
        return jsonify([d.dict() for d in devices]), 200  # ✅ Convert each object to a dictionary
    except Exception as e:
        app.logger.exception("Failed to fetch devices")
        return jsonify({"error": f"Failed to fetch devices: {str(e)}"}), 500

@app.route('/api/measurements', methods=['GET'])
def get_measurements():
    """ Fetch all measurements, ensuring datetime fields are JSON serializable """
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        measurements = db.measurement.find_many(order={"time": "desc"})

        # ✅ Convert objects to dictionaries & format time
        formatted_measurements = [
            {
                **m.dict(),  # Convert object to dict
                "time": m.time.isoformat() if isinstance(m.time, datetime) else m.time  # Convert `time` to string
            }
            for m in measurements
        ]

        return jsonify(formatted_measurements), 200

    except Exception as e:
        app.logger.exception("Failed to fetch measurements")
        return jsonify({"error": f"Failed to fetch measurements: {str(e)}"}), 500

@app.route('/')
def index():
    """ Home route displaying device and measurement count """
    if db is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        devices = db.device.find_many()
        measurements = db.measurement.find_many(order={"time": "desc"})

        device_count = len(devices) if devices else 0
        measurement_count = len(measurements) if measurements else 0

        return render_template("index.html",
                               device_count=device_count,
                               measurement_count=measurement_count,
                               measurements=measurements)
    except Exception as e:
        app.logger.exception("Failed to load index page")
        return jsonify({"error": f"Failed to load index: {str(e)}"}), 500

app.register_blueprint(tts_uplink_blueprint, url_prefix='/tts/uplink')

if __name__ == '__main__':
    if db is not None:
        app.run(debug=True, threaded=True)
    else:
        print("❌ Prisma is not connected. Flask will not start.")
