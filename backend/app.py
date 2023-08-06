from flask import Flask, request, jsonify
from flask_cors import CORS
from calendar_helper import Calendar
from settings import Settings
import requests
from notifications import Notifications
from pills import PillDatabase

app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

calendar = Calendar()
settings = Settings() # config.ini is created if it doesn't exist
notifications = Notifications()
pillDatabase = PillDatabase()

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
    result = notifications.notification("Test notification from backend", title="Test notification", priority="high", tags="white_check_mark")
    if result:
        response = {
            "status": "success",
        }
        return jsonify(response)
    else:
        response = {
            "status": "error",
        }
        return jsonify(response)
    
@app.route('/api/pills', methods=['GET', 'POST', 'PUT', 'DELETE'])
def pills():
    if request.method == 'GET':
        response = {
            "status": "success",
            "pills": pillDatabase.get_pills()
        }
        return jsonify(response)
    elif request.method == 'POST':
        data = request.get_json()
        pillDatabase.add_pill(data['name'], data['round'], data['number'], data['dispenser'])
        notifications.notification(f"{data['name']} added", title="New pill added", priority="default", tags="pill")
        response = {
            "status": "success",
        }
        return jsonify(response)
    elif request.method == 'PUT':
        data = request.get_json()
        pillDatabase.update_pill(data['id'], data['name'], data['round'], data['number'], data['dispenser'])
        notifications.notification(f"{data['name']} edited", title="Pill edited", priority="default", tags="pill")
        response = {
            "status": "success",
        }
        return jsonify(response)
    elif request.method == 'DELETE':
        data = request.get_json()
        pillDatabase.delete_pill(data['id'])
        notifications.notification(f"{data['name']} deleted", title="Pill deleted", priority="default", tags="pill")
        response = {
            "status": "success",
        }
        return jsonify(response)
    # otherwise return an http status code 405 (method not allowed)
    else:
        response = {
        "status": "error",
        "message": "Method not allowed"}
        return jsonify(response), 405

if __name__ == '__main__':
    notifications.notification("Daily Display is starting up", title="Backend started", priority="high", tags="rocket")
    app.run(debug=True)