#!/venv/bin/python3
# -*- coding: utf-8 -*-
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
from datetime import datetime, timedelta

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
            scheduler.remove_job(f"{round_name}_unlock")
        except:
            #print("Job not found")
            pass
        
        round_time = datetime.strptime(round['time'], "%H:%M").astimezone()
        round_hour = datetime.strftime(round_time, "%H")
        round_minute = datetime.strftime(round_time, "%M")

        scheduler.add_job(handle_round, 'cron', hour=round_hour, minute=round_minute, id=round_name, args=[round_name])

        # Unlock the dispenser early
        manual_dispense_time = settings.get_config_dict()['manual_dispense']
        unlock_time = round_time - timedelta(minutes=manual_dispense_time)
        unlock_hour = datetime.strftime(unlock_time, "%H")
        unlock_minute = datetime.strftime(unlock_time, "%M")

        scheduler.add_job(unlock_dispenser, 'cron', hour=unlock_hour, minute=unlock_minute, id=f"{round_name}_unlock", args=[round_name])
        
        #print(scheduler.get_job(round_name))

def handle_round(round_name):
    print(f"Handling round {round_name}")

    # Handle reciept printing
    reciept_rounds = settings.get_config_dict()['receipt_rounds']
    if round_name in reciept_rounds:
        print_calendar()

    # Handle pill dispense
    pills = pillDatabase.get_pills()
    for pill in pills:
        if round_name in pill['round']:
            dispenser.dispense_pill(pill['dispenser'], pill['number'])
            notifications.notification(f"{pill['name']} dispensed", title="Pill dispensed", priority="default", tags="pill")

    # Mark round as taken
    pillDatabase.set_round_taken_by_name(round_name, 1)

def unlock_dispenser(round_name):
    pillDatabase.set_round_taken_by_name(round_name, 0)

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
        "events": calendar.get_events_dict(calendar.get_today(), calendar.get_today() + timedelta(days=1))
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
    # get the next round
    next_round = pillDatabase.get_next_round()

    if next_round is None:
        response = {
            "status": "error",
            "message": "No rounds found"
        }
        return jsonify(response)
    
    if next_round['soon'] == True and next_round['taken'] == 0:
        response = {
        "status": "success",
        "warning": "wait",
        "pill_round": next_round['name'],
        "time_until": next_round['time_until']
        }
        return jsonify(response)
        
    if next_round['overdue'] == True and next_round['taken'] == 0:
        response = {
            "status": "success",
            "warning": "take",
            "pill_round": next_round['name'],
            "time_until": next_round['time_until']
        }
        return jsonify(response)
        
    if next_round['soon'] == False and next_round['overdue'] == False and next_round['taken'] == 0:
        response = {
            "status": "success",
            "warning": "none",
            "pill_round": next_round['name'],
            "time_until": next_round['time_until']
        }
        return jsonify(response)
    
    response = {
            "status": "error",
            "message": "No rounds found"
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
            # rerun schedule_rounds to update the schedule
            schedule_rounds()

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
    print_calendar()
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

@app.route('/api/mark_round_taken', methods=['GET'])
def mark_round_taken():
    # Trying to figure out a way to mark the current round taken
    # whether that's the next manual round, or the current overdue round 
    next_round = pillDatabase.get_next_round()
    if next_round is not None:
        pillDatabase.set_round_taken_by_name(next_round['name'], 1)
        response = {
            "status": "success",
        }
        return jsonify(response)
    else:
        response = {
            "status": "error",
            "message": "No rounds found"
        }
        return jsonify(response)

@app.route('/api/cycle_dispenser', methods=['POST'])
def cycle_dispenser():
    data = request.get_json()
    try:
        dispenser.cycle_dispenser(data['index'])
        response = {
            "status": "success",
        }
    except:
        response = {
            "status": "error",
        }
    return jsonify(response)

@app.route('/api/shutdown', methods=['GET'])
def shutdown():
    os.system("shutdown -h now")
    response = {
        "status": "success",
    }
    return jsonify(response)

def print_calendar():
    date = calendar.get_date()
    calendar_events = calendar.get_events_list(calendar.get_today(), calendar.get_today() + timedelta(days=1))
    printer.print_calendar(calendar_events, date)

if __name__ == '__main__':
    notifications.notification("Daily Display is starting up", title="Backend started", priority="default", tags="rocket")
    app.run(debug=True, host='0.0.0.0')