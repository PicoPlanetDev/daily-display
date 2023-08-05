from flask import Flask, request, jsonify
from flask_cors import CORS
from calendar_helper import Calendar
from settings import Settings
import requests

app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

calendar = Calendar()
settings = Settings() # config.ini is created if it doesn't exist

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

@app.route('/api/version', methods=['GET'])
def get_version():
    response = {
        "status": "success",
        "version": "0.0.1"
    }
    return jsonify(response)

@app.route('/api/pill_warning', methods=['GET'])
def pill_warning():
    response = {
        "status": "success",
        "warning": "none",
        "pill_round": "morning",
    }
    return jsonify(response)

@app.route('/api/settings', methods=['GET', 'POST'])
def get_settings():
    if request.method == 'GET':
        response = {
            "status": "success",
            "settings": settings.get_config_dict()
        }
        return jsonify(response)
    elif request.method == 'POST':
        data = request.get_json()
        if settings.update_config(data):
            response = {
                "status": "success",
            }
            return jsonify(response)
        else:
            response = {
                "status": "error",
            }
            return jsonify(response)
    
    # otherwise return an http status code 405 (method not allowed)
    else:
        response = {
        "status": "error",
        "message": "Method not allowed"}
        return jsonify(response), 405

@app.route('/api/test_notification', methods=['GET'])
def test_notify():
    post_url = settings.get_config_dict()["notification_url"]
    requests.post(post_url, data=r"Test notification ✅".encode(encoding='utf-8'))
    response = {
        "status": "success",
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)