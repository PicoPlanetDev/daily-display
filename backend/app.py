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
    # read
    if request.method == 'GET':
        response = {
            "status": "success",
            "pills": pillDatabase.get_pills()
        }
        return jsonify(response)
    
    # create
    elif request.method == 'POST':
        data = request.get_json()
        try:
            pillDatabase.add_pill(
                str(data['name']).strip(),
                str(data['round']).strip(),
                int(str(data['number']).strip()),
                int(str(data['dispenser']).strip())
                )
        except:
            response = {
                "status": "error",
                "message": "Invalid data"
            }
            return jsonify(response)
        else:
            notifications.notification(f"{data['name']} added", title="New pill added", priority="default", tags="pill")
            response = {
                "status": "success",
            }
            return jsonify(response)

    # update    
    elif request.method == 'PUT':
        data = request.get_json()
        try:
            pillDatabase.update_pill(
                int(str(data['id']).strip()),
                str(data['name']).strip(),
                str(data['round']).strip(),
                int(str(data['number']).strip()),
                int(str(data['dispenser']).strip())
                )
        except:
            response = {
                "status": "error",
                "message": "Invalid data"
            }
            return jsonify(response)
        else:
            notifications.notification(f"{data['name']} edited", title="Pill edited", priority="default", tags="pill")
            response = {
                "status": "success",
            }
            return jsonify(response)

    # delete    
    elif request.method == 'DELETE':
        data = request.get_json()
        try:
            pillDatabase.delete_pill(data['id'])
        except:
            response = {
                "status": "error",
                "message": "Invalid data"
            }
            return jsonify(response)
        else:
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

@app.route('/api/rounds', methods=['GET', 'POST', 'PUT', 'DELETE'])
def rounds():
    # read
    if request.method == 'GET':
        response = {
            "status": "success",
            "rounds": pillDatabase.get_rounds()
        }
        return jsonify(response)
    
    # create
    elif request.method == 'POST':
        data = request.get_json()
        try:
            pillDatabase.add_round(
                str(data['name']).strip(),
                str(data['time']).strip()
                )
        except:
            response = {
                "status": "error",
                "message": "Invalid data"
            }
            return jsonify(response)
        else:
            notifications.notification(f"{data['name']} added", title="New round added", priority="default", tags="clock4")
            response = {
                "status": "success",
            }
            return jsonify(response)
        
    # update
    elif request.method == 'PUT':
        data = request.get_json()
        try:
            pillDatabase.update_round(
                int(str(data['id']).strip()),
                    str(data['name']).strip(),
                    str(data['time']).strip()
                    )
        except:
            response = {
                "status": "error",
                "message": "Invalid data"
            }
            return jsonify(response)
        else:
            notifications.notification(f"{data['name']} edited", title="Round edited", priority="default", tags="clock4")
            response = {
                "status": "success",
            }
            return jsonify(response)
        
    # delete
    elif request.method == 'DELETE':
        data = request.get_json()
        try:
            pillDatabase.delete_round(
                int(str(data['id']).strip())
                )
        except:
            response = {
                "status": "error",
                "message": "Invalid data"
            }
            return jsonify(response)
        else:
            notifications.notification(f"{data['name']} deleted", title="Round deleted", priority="default", tags="clock4")
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

@app.route('/api/print_receipt', methods=['GET'])
def print_receipt():
    response = {
        "status": "success",
    }
    return jsonify(response)

if __name__ == '__main__':
    notifications.notification("Daily Display is starting up", title="Backend started", priority="high", tags="rocket")
    app.run(debug=True)