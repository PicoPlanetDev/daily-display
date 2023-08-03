from flask import Flask, request, jsonify
from flask_cors import CORS
from calendar_helper import Calendar

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

calendar = Calendar()

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify('pong')

@app.route('/api/datetime', methods=['GET'])
def get_datetimes():
    response = {
        "date": calendar.get_date(),
        "time": calendar.get_time()
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)