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
    
    def get_events(self, start_date=datetime.today(), end_date=datetime.today()+timedelta(days=1)):
        calendar_events = icalevents.events(self.url, start=start_date, end=end_date)

        events_list = []

        for event in calendar_events:
            event_type = None
            if "TASK" in str(event.summary):
                event_type = "TASK"

            event_title = str(event.summary) # potentially with the LABELS
            if event_type is not None:
                event_title = str(event.summary).replace(event_type, "").strip() # no type label, no leading/trailing white

            event_start = datetime.strptime(str(event.start), "%Y-%m-%d %H:%M:%S%z") # get a datetime object of the event starting time
            
            event_start_full = datetime.strftime(event_start, "%c") # make it readable
            event_start_time = datetime.strftime(event_start, "%-I:%M %p") # make it readable

            event_uid = str(event.uid)

            event_timestamp = event_start.timestamp()

            event_info_dict = {
                "title": event_title,
                "type": event_type,#"TASK",
                "datetime": event_start_full,
                "uid": event_uid,
                "all_day": event.all_day,
                "time_string": event_start_time,
                "timestamp": event_timestamp
            }

            events_list.append(event_info_dict)

        # convert to dict with keys as uid
        events_dict = {}
        for event in events_list:
            events_dict[event["uid"]] = event

        return events_dict