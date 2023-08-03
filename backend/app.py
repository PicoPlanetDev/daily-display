from flask import Flask, request, jsonify
from flask_cors import CORS
from calendar_helper import Calendar

app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

calendar = Calendar()

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify('pong')

@app.route('/api/datetime', methods=['GET'])
def get_datetimes():
    response = {
        "status": "success",
        "date": calendar.get_date(),
        "time": calendar.get_time()
    }
    return jsonify(response)

@app.route('/api/events', methods=['GET'])
def get_events():
    response = {
        "status": "success",
        "events": calendar.get_events()
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)