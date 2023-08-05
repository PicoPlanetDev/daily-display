from icalevents import icalevents
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import re

def pluralize(string, count):
    if count == 1:
        return string
    else:
        return string + "s"

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
    
    def get_events(self, start_date=datetime.today()-timedelta(days=0), end_date=datetime.today()+timedelta(days=1)):
        calendar_events = icalevents.events(self.url, start=start_date, end=end_date)

        events_list = []

        for event in calendar_events:
            event_type = None
            lower_summary = str(event.summary).lower()
            if "task" in lower_summary:
                event_type = "Task"
            elif "event" in lower_summary:
                event_type = "Event"
            elif "appointment" in lower_summary:
                event_type = "Appointment"

            event_title = str(event.summary) # potentially with the LABELS
            if event_type is not None:
                #event_title = str(event.summary).replace(event_type, "").strip() # no type label, no leading/trailing white
                #event_title = re.sub(r"\b" + event_type + r"\b", "", str(event.summary)).strip() # no type label, no leading/trailing white
                compiled = re.compile(re.escape(event_type), re.IGNORECASE)
                event_title = compiled.sub("", str(event.summary)).strip() # no type label, no leading/trailing white

            event_start = datetime.strptime(str(event.start), "%Y-%m-%d %H:%M:%S%z") # get a datetime object of the event starting time
            
            # make sure the timezones are correct
            event_start = event_start.astimezone(tz=None) # convert to local timezone

            event_start_full = datetime.strftime(event_start, "%c") # make it readable
            event_start_time = datetime.strftime(event_start, "%-I:%M %p") # make it readable

            event_uid = str(event.uid)

            event_timestamp = event_start.timestamp()

            # time until event
            event_time_until = event_start - datetime.now().astimezone()+timedelta(hours=-12)
            event_time_until_formatted = ""
            if event_time_until.days > 0:
                event_time_until_formatted = str(event_time_until.days) + pluralize(" day", event_time_until.days)
            elif event_time_until.seconds >= 3600:
                event_time_until_formatted = str(event_time_until.seconds // 3600) + pluralize(" hour", event_time_until.seconds // 3600)
            elif event_time_until.seconds >= 60:
                event_time_until_formatted = str(event_time_until.seconds // 60) + pluralize(" minute", event_time_until.seconds // 60)
            elif event_time_until.seconds < 60:
                event_time_until_formatted = "less than a minute"

            event_time_until_formatted = "in " + event_time_until_formatted

            event_info_dict = {
                "title": event_title,
                "type": event_type,
                #"type": "Task",
                "datetime": event_start_full,
                "uid": event_uid,
                "all_day": event.all_day,
                "time_string": event_start_time,
                "timestamp": event_timestamp,
                "up_next": False,
                "time_until": event_time_until_formatted
            }

            events_list.append(event_info_dict)

        # sort the events by timestamp
        events_list.sort(key=lambda x: x["timestamp"])

        # find the soonest upcoming event, and mark it as up_next
        now_timestamp = (datetime.now()+timedelta(hours=-12)).astimezone().timestamp()
        found_up_next = False
        for event in events_list:
            if event["timestamp"] > now_timestamp and not found_up_next:
                event["up_next"] = True
                found_up_next = True
                break

        # convert to dict with keys as uid
        events_dict = {}
        for event in events_list:
            events_dict[event["uid"]] = event
        
        return events_dict