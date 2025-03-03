from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth

import sqlite3

api_key = "QoFahtA2ut49qCuVhZjGk2HNy2tJex"

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'username'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
basic_auth = BasicAuth(app)

@app.route('/')
def index():
    return "Hello, Welcome to Derek's Allotment"

@app.route('/uplink/message', methods=['POST'])
@basic_auth.required
def uplink_message():
    if request.method == 'POST':
        conn = db_connection()
        cursor = conn.cursor()

        try:
            print(request.args)

            # cursor.execute("INSERT INTO books (author, title) VALUES (?, ?)", (new_author, new_title))
            # conn.commit()
            return jsonify({"message": "Book added successfully"}), 201
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

@app.route('/uplink/payload', methods=['POST'])
def uplink_payload():
    if request.method == 'POST':
        try:
            print(request.args)
            return jsonify({"message": "Book added successfully"}), 201
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('allotment_weather.sqlite')
    except sqlite3.Error as e:
        print("Error while connecting to SQLite database:", e)
    return conn

if __name__ == '__main__':
    app.run(debug=True)