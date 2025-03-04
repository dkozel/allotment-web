from flask import Flask, render_template
from flask_basicauth import BasicAuth
from prisma import Prisma, register
from prisma.models import Device, Measurement

from auth import basic_auth, init_basic_auth
from routes.tts_uplink import tts_uplink_blueprint

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)
init_basic_auth(app)

@app.route('/')
def index():
    try:
        # Query all devices and measurements.
        devices = Device.prisma().find_many()
        measurements = Measurement.prisma().find_many(order={'time': 'desc'})
    except Exception as e:
        # Return an error page if there is a problem.
        return f"Error retrieving data: {str(e)}", 500

    # Count the number of devices and measurements.
    device_count = len(devices)
    measurement_count = len(measurements)
    
    # Render the homepage template with the counts and measurement data.
    return render_template("index.html", 
                           device_count=device_count, 
                           measurement_count=measurement_count, 
                           measurements=measurements)

app.register_blueprint(tts_uplink_blueprint, url_prefix='/tts/uplink')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)