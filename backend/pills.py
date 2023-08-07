from notifications import Notifications
import sqlite3

class PillDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('pills.db', check_same_thread=False)
        self.ensure_database()
    
    def get_cursor(self):
        return self.conn.cursor()

    def ensure_database(self):
        # Create the table if it doesn't exist
        self.get_cursor().execute('''CREATE TABLE IF NOT EXISTS pills
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, round TEXT, taken INTEGER, number INTEGER, dispenser INTEGER)''')
        self.conn.commit()

        # Create the rounds table if it doesn't exist
        self.get_cursor().execute('''CREATE TABLE IF NOT EXISTS rounds
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time TEXT)''')
        self.conn.commit()
    
    def get_pills(self):
        self.get_cursor().execute("SELECT * FROM pills")
        result = self.get_cursor().fetchall()
        pills = []
        for pill in result:
            pills.append({
                "id": pill[0],
                "name": pill[1],
                "round": pill[2],
                "taken": pill[3],
                "number": pill[4],
                "dispenser": pill[5]
            })
        return pills
    
    def get_rounds(self):
        self.get_cursor().execute("SELECT * FROM rounds")
        result = self.get_cursor().fetchall()
        rounds = []
        for round in result:
            rounds.append({
                "id": round[0],
                "name": round[1],
                "time": round[2]
            })
        return rounds
    
    def add_pill(self, name, round, number, dispenser):
        self.get_cursor().execute("INSERT INTO pills (name, round, taken, number, dispenser) VALUES (?, ?, ?, ?, ?)", (name, round, 0, number, dispenser))
        self.conn.commit()

    def add_round(self, name, time):
        self.get_cursor().execute("INSERT INTO rounds (name, time) VALUES (?, ?)", (name, time))
        self.conn.commit()
    
    def delete_pill(self, id):
        self.get_cursor().execute("DELETE FROM pills WHERE id=?", (id,))
        self.conn.commit()
    
    def delete_round(self, id):
        self.get_cursor().execute("DELETE FROM rounds WHERE id=?", (id,))
        self.conn.commit()
    
    def update_pill(self, id, name, round, number, dispenser):
        self.get_cursor().execute("UPDATE pills SET name=?, round=?, number=?, dispenser=? WHERE id=?", (name, round, number, dispenser, id))
        self.conn.commit()
    
    def update_round(self, id, name, time):
        self.get_cursor().execute("UPDATE rounds SET name=?, time=? WHERE id=?", (name, time, id))
        self.conn.commit()
    
    def set_pill_status(self, id, taken):
        self.get_cursor().execute("UPDATE pills SET taken=? WHERE id=?", (taken, id))
        self.conn.commit()