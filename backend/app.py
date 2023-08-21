from flask import Flask, request, jsonify
from flask_cors import CORS
from calendar_helper import Calendar
from settings import Settings
import requests
from notifications import Notifications
from pills import PillDatabase
from printer import Printer
import os
import subprocess
import qrcode
import local_ip
from apscheduler.schedulers.background import BackgroundScheduler
from dispenser import Dispenser
from tzlocal import get_localzone

tz = get_localzone()
scheduler = BackgroundScheduler(timezone=tz)
scheduler.start()

app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

calendar = Calendar()
settings = Settings() # config.ini is created if it doesn't exist
notifications = Notifications()
pillDatabase = PillDatabase()
printer = Printer()
dispenser = Dispenser(i2c_bus=3, i2c_address=0x40)

def schedule_rounds():
    for round in pillDatabase.get_rounds():
        round_name = round['name']
        try:
            scheduler.remove_job(round_name)
        except:
            print("Job not found")
        
        round_time = round['time'].split(":")
        round_hour = int(round_time[0])
        round_minute = int(round_time[1])
        #print(f"Added job {name} at {round_hour}:{round_minute}")
        scheduler.add_job(handle_round, 'cron', hour=round_hour, minute=round_minute, id=round_name, args=[round_name])
        print(scheduler.get_job(round_name))

def handle_round(round_name):
    print(f"Handling round {round_name}")

    # Handle reciept printing
    reciept_rounds = settings.get_config_dict()['receipt_rounds']
    if round_name in reciept_rounds:
        print_receipt()

    # Handle pill dispense
    pills = pillDatabase.get_pills()
    for pill in pills:
        if round_name in pill['round']:
            dispenser.dispense_pill(pill['dispenser'], pill['number'])
            notifications.notification(f"{pill['name']} dispensed", title="Pill dispensed", priority="default", tags="pill")

schedule_rounds()

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
        "events": calendar.get_events_dict()
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
            schedule_rounds()
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
            schedule_rounds()
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
            schedule_rounds()
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
    date = calendar.get_date()
    calendar_events = calendar.get_events_list()
    printer.print_calendar(calendar_events, date)
    response = {
        "status": "success",
    }
    return jsonify(response)

@app.route('/api/feed_printer', methods=['GET'])
def feed_printer():
    printer.end()
    response = {
        "status": "success",
    }
    return jsonify(response)

@app.route('/api/print_qr', methods=['GET'])
def print_qr():
    # get local ip address
    ip = local_ip.get_ip()
    link = f"http://{ip}:5173"
    qr = qrcode.make(link)
    printer.print_qr(qr, link, "Access on the local network")

    # attempt to get tailscale ip address
    result = subprocess.check_output(['tailscale', 'ip']).decode("utf-8")
    if "command not found" not in result:
        ip = result.split()[0]
        link = f"http://{ip}:5173"
        qr = qrcode.make(link)
        printer.print_qr(qr, link, "Access with Tailscale enabled")

    response = {
        "status": "success",
    }
    return jsonify(response)

if __name__ == '__main__':
    notifications.notification("Daily Display is starting up", title="Backend started", priority="default", tags="rocket")
    app.run(debug=True, host='0.0.0.0')