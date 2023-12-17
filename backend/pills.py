from notifications import Notifications
import sqlite3
from datetime import datetime
import calendar_helper
import settings

class PillDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('pills.db', check_same_thread=False)
        self.cur = self.get_cursor()
        self.ensure_database()
        self.calendar = calendar_helper.Calendar()
        self.config = settings.Settings()
    
    def get_cursor(self):
        return self.conn.cursor()

    def ensure_database(self):
        # Create the table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS pills
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, round TEXT, number INTEGER, dispenser INTEGER, dispensed INTEGER, taken INTEGER)''')
        self.conn.commit()

        # Create the rounds table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS rounds
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time TEXT, taken INTEGER)''')
        self.conn.commit()

        # Create the dispensers table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS dispensers
            (id INTEGER PRIMARY KEY AUTOINCREMENT, dispenser_index NUMBER, servo_min INTEGER, servo_max INTEGER, angle_default INTEGER, angle_chute INTEGER, smooth_duration REAL, step_time REAL, smooth_enabled INTEGER, sensor_pin INTEGER, sensor_enabled INTEGER)''')
        self.conn.commit()
        # Create the default dispensers if they don't exist
        self.create_default_dispensers()

    def create_default_dispensers(self):
        # Check how many dispensers there are
        dispensers = self.get_dispensers()
        if len(dispensers) < 16:
            # Create the default dispensers
            for i in range(16):
                self.add_dispenser(i, 100, 500, 90, 0, 1, 0.01, 1, -1, 0)
    
    def get_pills(self):
        self.cur.execute("SELECT * FROM pills")
        result = self.cur.fetchall()
        pills = []
        for pill in result:
            pills.append({
                "id": pill[0],
                "name": pill[1],
                "round": pill[2],
                "number": pill[3],
                "dispenser": pill[4],
                "dispensed": pill[5],
                "taken": pill[6]
            })
        return pills
    
    def get_rounds(self):
        self.cur.execute("SELECT * FROM rounds")
        result = self.cur.fetchall()
        rounds = []
        for round in result:
            rounds.append({
                "id": round[0],
                "name": round[1],
                "time": round[2],
                "taken": round[3]
            })
        return rounds
    
    def get_dispensers(self):
        self.cur.execute("SELECT * FROM dispensers")
        result = self.cur.fetchall()
        dispensers = []
        for dispenser in result:
            dispensers.append({
                "id": dispenser[0],
                "index": dispenser[1],
                "servo_min": dispenser[2],
                "servo_max": dispenser[3],
                "angle_default": dispenser[4],
                "angle_chute": dispenser[5],
                "smooth_duration": dispenser[6],
                "step_time": dispenser[7],
                "smooth_enabled": dispenser[8],
                "sensor_pin": dispenser[9],
                "sensor_enabled": dispenser[10]
            })
        return dispensers
    
    def get_all(self):
        return {
            "pills": self.get_pills(),
            "rounds": self.get_rounds(),
            "dispensers": self.get_dispensers()
        }
    
    def get_dispenser(self, index):
        self.cur.execute("SELECT * FROM dispensers WHERE dispenser_index=?", (index,))
        result = self.cur.fetchone()
        if result is None:
            return None
        return {
            "id": result[0],
            "index": result[1],
            "servo_min": result[2],
            "servo_max": result[3],
            "angle_default": result[4],
            "angle_chute": result[5],
            "smooth_duration": result[6],
            "step_time": result[7],
            "smooth_enabled": result[8],
            "sensor_pin": result[9],
            "sensor_enabled": result[10]
        }

    def get_next_round(self):
        now = datetime.now(tz=self.calendar.timezone)
        # if the previous round has not been taken, return it
        self.cur.execute("SELECT * FROM rounds WHERE time < ? AND taken = 0 ORDER BY time DESC LIMIT 1", (now.strftime("%H:%M"),))
        result = self.cur.fetchone() # will return in order of id, name, time, taken
        if result is not None:
            hours, minutes = str(result[2]).split(":")
            hours = int(hours)
            minutes = int(minutes)
            
            time_until = now.replace(hour=hours, minute=minutes, second=0, microsecond=0) - now
            time_until_formatted = calendar_helper.format_time_until(time_until)

            return {
                "id": result[0],
                "name": result[1],
                "time": result[2],
                "time_until": time_until_formatted,
                "taken": result[3],
                "overdue": True,
                "soon": True,
            }

        # otherwise move on to the next round
        self.cur.execute("SELECT * FROM rounds WHERE time > ? ORDER BY time ASC LIMIT 1", (now.strftime("%H:%M"),))
        result = self.cur.fetchone()
        if result is None:
            return None

        hours, minutes = str(result[2]).split(":")
        hours = int(hours)
        minutes = int(minutes)

        time_until = now.replace(hour=hours, minute=minutes, second=0, microsecond=0) - now
        # check if the round is within the unlock time
        if time_until.total_seconds() < self.config.get_config_dict()["manual_dispense"] * 60: # convert minutes to seconds
            time_until_formatted = calendar_helper.format_time_until(time_until)

            return {
                "id": result[0],
                "name": result[1],
                "time": result[2],
                "time_until": time_until_formatted,
                "taken": result[3],
                "overdue": False,
                "soon": True,
            }
        else:
            return {
                "id": None,
                "name": result[1],
                "time": result[2],
                "time_until": None,
                "taken": result[3],
                "overdue": False,
                "soon": False,
            }

    # --- Create ---
    def add_pill(self, name: str, round: str, number: int, dispenser: int):
        """Adds a pill to the database

        Args:
            name (str): The pill's name
            round (str): The rounds the pill is taken in
            number (int): The number of pills to dispense in each round
            dispenser (int): The index of the dispenser to use
        """
        self.cur.execute("INSERT INTO pills (name, round, number, dispenser, dispensed, taken) VALUES (?, ?, ?, ?, 0, 0)", (name, round, number, dispenser))
        self.conn.commit()

    def add_round(self, name: str, time: str):
        """Adds a round to the database

        Args:
            name (str): The round's name
            time (str): The time the round is taken, in the format hh:mm (24 hour)
        """
        self.cur.execute("INSERT INTO rounds (name, time, taken) VALUES (?, ?, ?)", (name, time, 0))
        self.conn.commit()

    def add_dispenser(self, index: int, servo_min: int, servo_max: int, angle_default, angle_chute, smooth_duration: float, step_time: float, smooth_enabled: int, sensor_pin: int, sensor_enabled: int):
        """Adds a dispenser to the database

        Args:
            index (int): The index of the dispenser
            servo_min (int): The minimum angle of the servo
            servo_max (int): The maximum angle of the servo
            angle_default (int): The default angle of the servo
            angle_chute (int): The angle of the servo when the chute is open
            smooth_duration (float): The duration of the smooth movement
            step_time (float): The time between each step of the smooth movement
            smooth_enabled (int): Whether or not the smooth movement is enabled (1 or 0)
            sensor_pin (int): The GPIO pin of the sensor
            sensor_enabled (int): Whether or not the sensor is enabled (1 or 0)
        """
        self.cur.execute("INSERT INTO dispensers (dispenser_index, servo_min, servo_max, angle_default, angle_chute, smooth_duration, step_time, smooth_enabled, sensor_pin, sensor_enabled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, servo_min, servo_max, angle_default, angle_chute, smooth_duration, step_time, smooth_enabled, sensor_pin, sensor_enabled))
        self.conn.commit()
    
    # --- Delete ---
    def delete_pill(self, id):
        self.cur.execute("DELETE FROM pills WHERE id=?", (id,))
        self.conn.commit()
    
    def delete_round(self, id):
        self.cur.execute("DELETE FROM rounds WHERE id=?", (id,))
        self.conn.commit()

    def delete_dispenser(self, id):
        self.cur.execute("DELETE FROM dispensers WHERE id=?", (id,))
        self.conn.commit()
    
    # --- Update ---
    def update_pill(self, id, name: str, round: str, number: int, dispenser: int):
        self.cur.execute("UPDATE pills SET name=?, round=?, number=?, dispenser=? WHERE id=?", (name, round, number, dispenser, id))
        self.conn.commit()
    
    def update_round(self, id, name: str, time: str):
        self.cur.execute("UPDATE rounds SET name=?, time=? WHERE id=?", (name, time, id))
        self.conn.commit()

    def update_dispenser(self, id, index: int, servo_min: int, servo_max: int, angle_default, angle_chute, smooth_duration: float, step_time: float, smooth_enabled: int, sensor_pin: int, sensor_enabled: int):
        self.cur.execute("UPDATE dispensers SET dispenser_index=?, servo_min=?, servo_max=?, angle_default=?, angle_chute=?, smooth_duration=?, step_time=?, smooth_enabled=?, sensor_pin=?, sensor_enabled=? WHERE id=?", (index, servo_min, servo_max, angle_default, angle_chute, smooth_duration, step_time, smooth_enabled, sensor_pin, sensor_enabled, id))
        self.conn.commit()
    
    # --- Round-specific tasks ---
    def set_round_taken(self, id, taken):
        self.cur.execute("UPDATE rounds SET taken=? WHERE id=?", (taken, id))
        self.conn.commit()
    
    def set_round_taken_by_name(self, name, taken):
        self.cur.execute("UPDATE rounds SET taken=? WHERE name=?", (taken, name))
        self.conn.commit()

    def get_rounds_taken(self):
        self.cur.execute("SELECT COUNT(*) FROM rounds WHERE taken = 1")
        result = self.cur.fetchone()
        return True if result[0] == 1 else False
    
    def set_round_not_dispensed(self, round_name: str):
        """Sets all the pills in the specified round to not dispensed

        Args:
            round_name (str): The name of the round to set to not dispensed
        """        
        # Maybe a sketchy way to handle the round_name being only one of potentially multiple rounds
        # Split the round_name parameter into individual rounds
        rounds = round_name.split(',')

        # Create a parameter placeholder for each round
        placeholders = ', '.join('?' for round in rounds)

        # Create the SQL query
        query = f"UPDATE pills SET dispensed=0 WHERE round IN ({placeholders})"

        # Execute the SQL query with the rounds as parameters
        self.cur.execute(query, rounds)
        self.conn.commit()

    # Pill dispensed and taken
    def set_pill_dispensed(self, dispenser_index):
        # TODO: doesn't support multiple pills per round
        self.cur.execute("UPDATE pills SET dispensed=1 WHERE dispenser=?", (dispenser_index,))
        self.conn.commit()
        
        # Get the next round
        next_round = self.get_next_round()
        if next_round is not None:
            # see if all the pills have been dispensed
            self.cur.execute("SELECT COUNT(*) FROM pills WHERE round=? AND dispensed=0", (next_round["name"],))
            result = self.cur.fetchone()
            if result[0] == 0:
                # set the round as taken
                self.set_round_taken_by_name(next_round["name"], 1)
                # send a notification
                self.notifications = Notifications()
                self.notifications.notification(f"Round {next_round['name']} taken", "Daily Display", "default")
    
    # def set_pill_taken(self, dispenser_index):
    #     self.cur.execute("UPDATE pills SET taken=1 WHERE dispenser=?", (dispenser_index,))
    #     self.conn.commit()
    
    def get_pill(self, dispenser_index):
        """Gets the pill from the database that is dispensed by the specified dispenser

        Args:
            dispenser_index (int): The dispenser index to get the pill for

        Returns:
            dict: The pill
        """
        self.cur.execute("SELECT * FROM pills WHERE dispenser=?", (dispenser_index,))
        result = self.cur.fetchone()
        return {
            "id": result[0],
            "name": result[1],
            "round": result[2],
            "number": result[3],
            "dispenser": result[4],
            "dispensed": result[5],
            "taken": result[6]
        }
