from notifications import Notifications
import sqlite3
import datetime
import calendar_helper

class PillDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('pills.db', check_same_thread=False)
        self.cur = self.get_cursor()
        self.ensure_database()
    
    def get_cursor(self):
        return self.conn.cursor()

    def ensure_database(self):
        # Create the table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS pills
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, round TEXT, number INTEGER, dispenser INTEGER)''')
        self.conn.commit()

        # Create the rounds table if it doesn't exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS rounds
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time TEXT, taken INTEGER)''')
        self.conn.commit()
    
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
                "dispenser": pill[4]
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
    
    def get_pills_and_rounds(self):
        return {
            "pills": self.get_pills(),
            "rounds": self.get_rounds()
        }
    
    def get_next_round(self):
        now = datetime.datetime.now().astimezone()
        # if the previous round has not been taken, return it
        self.cur.execute("SELECT * FROM rounds WHERE time < ? AND taken = 0 ORDER BY time DESC LIMIT 1", (now.strftime("%H:%M"),))
        result = self.cur.fetchone()
        if result is not None:
            time_until = datetime.datetime.strptime(result[2], "%H:%M") - now
            time_until_formatted = calendar_helper.format_time_until(time_until)

            return {
                "id": result[0],
                "name": result[1],
                "time": result[2],
                "time_until": time_until_formatted,
                "taken": result[3],
                "overdue": True,
            }

        # otherwise move on to the next round
        self.cur.execute("SELECT * FROM rounds WHERE time > ? ORDER BY time ASC LIMIT 1", (now.strftime("%H:%M"),))
        result = self.cur.fetchone()
        if result is None:
            return None

        time_until = datetime.datetime.strptime(result[2], "%H:%M") - now
        time_until_formatted = calendar_helper.format_time_until(time_until)

        return {
            "id": result[0],
            "name": result[1],
            "time": result[2],
            "time_until": time_until_formatted,
            "taken": result[3],
            "overdue": False,
        }


    def add_pill(self, name, round, number, dispenser):
        self.cur.execute("INSERT INTO pills (name, round, number, dispenser) VALUES (?, ?, ?, ?)", (name, round, number, dispenser))
        self.conn.commit()

    def add_round(self, name, time):
        self.cur.execute("INSERT INTO rounds (name, time, taken) VALUES (?, ?, ?)", (name, time, 0))
        self.conn.commit()
    
    def delete_pill(self, id):
        self.cur.execute("DELETE FROM pills WHERE id=?", (id,))
        self.conn.commit()
    
    def delete_round(self, id):
        self.cur.execute("DELETE FROM rounds WHERE id=?", (id,))
        self.conn.commit()
    
    def update_pill(self, id, name, round, number, dispenser):
        self.cur.execute("UPDATE pills SET name=?, round=?, number=?, dispenser=? WHERE id=?", (name, round, number, dispenser, id))
        self.conn.commit()
    
    def update_round(self, id, name, time):
        self.cur.execute("UPDATE rounds SET name=?, time=? WHERE id=?", (name, time, id))
        self.conn.commit()
    
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
