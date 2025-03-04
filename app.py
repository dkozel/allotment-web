from flask import Flask
from flask_basicauth import BasicAuth
from prisma import Prisma, register
from auth import basic_auth, init_basic_auth
from routes.tts_uplink import tts_uplink_blueprint

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)
init_basic_auth(app)

@app.route('/')
def index():
    return "Hello, Welcome to Derek's Allotment"

app.register_blueprint(tts_uplink_blueprint, url_prefix='/tts/uplink')

if __name__ == '__main__':
    app.run(debug=True, port=8080, threaded=True)