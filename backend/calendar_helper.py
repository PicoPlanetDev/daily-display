from icalevents import icalevents
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

class Calendar():
    def __init__(self):
        self.url = self.get_url()

    def get_url(self):
        load_dotenv()
        return os.getenv("SECRET_ICAL_URL")

    def get_date(self, format="%A, %b %-d"):
        return datetime.today().strftime(format)
    
    def get_time(self, format="%-I:%M %p"):
        return datetime.today().strftime(format)