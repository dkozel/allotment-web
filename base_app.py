from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from prisma import Prisma, register

db = Prisma()
db.connect()
register(db)

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)

@app.route('/')
def index():
    return "Hello, Welcome to Derek's Allotment"

@app.route('/tts/uplink/message', methods=['POST'])
@basic_auth.required
def uplink_message():
    if request.method == 'POST':
        try:
            print(request.args)
            return jsonify({"message": "Measurement added successfully"}), 201
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

@app.route('/tts/uplink/payload', methods=['POST'])
@basic_auth.required
def uplink_payload():
    if request.method == 'POST':
        try:
            print(request.args)
            return jsonify({"message": "Measurement added successfully"}), 201
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)