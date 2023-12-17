from icalevents import icalevents
from datetime import datetime, timedelta
import re
from settings import Settings
import pytz

def pluralize(string, count):
    """Automatically adds an 's' to the end of a string if the count is not 1

    Args:
        string (str): The string to pluralize
        count (int): The count to use (1 or anything else)

    Returns:
        str: The pluralized string
    """
    if count == 1:
        return string
    else:
        return string + "s"

def format_time_until(time_until):
    """Return a friendly string of the time until the event

    Args:
        time_until (datetime): Time until the event

    Returns:
        str: The formatted string of the time until the event
    """
    # print(f"time_until: {time_until}")
    time_until_formatted = ""
    if time_until.days > 0:
        time_until_formatted = str(time_until.days) + pluralize(" day", time_until.days)
    elif time_until.seconds >= 3600:
        time_until_formatted = str(time_until.seconds // 3600) + pluralize(" hour", time_until.seconds // 3600)
    elif time_until.seconds >= 60:
        time_until_formatted = str(time_until.seconds // 60) + pluralize(" minute", time_until.seconds // 60)
    elif time_until.seconds < 60:
        time_until_formatted = "less than a minute"
    return time_until_formatted

class Calendar():
    def __init__(self):
        self.settings = Settings()
        self.url = self.get_url()
        self.timezone = pytz.timezone(self.settings.get_config_dict()["timezone"])

    def get_today(self):
        """Return a datetime object of today at midnight

        Returns:
            datetime: Datetime object of today at midnight
        """        
        # return a datetime object of today at midnight
        return self.timezone.localize(datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0))

    def get_url(self):
        """Return the calendar url from the config

        Returns:
            str: Calendar url
        """
        return self.settings.config.get("Calendar", "calendar_url")

    # These are the same function but with different defaults (stupid)
    def get_date(self, format="%A, %b %-d"):
        """Return the datetime in the specified format

        Args:
            format (str, optional): strftime format. Defaults to "%A, %b %-d".

        Returns:
            str: Datetime formattted as a string
        """        
        return datetime.now(tz=self.timezone).strftime(format)
    
    def get_time(self, format="%-I:%M %p"):
        """Return the datetime in the specified format

        Args:
            format (str, optional): strftime format. Defaults to "%-I:%M %p".

        Returns:
            str: Datetime formattted as a string
        """   
        return datetime.now(tz=self.timezone).strftime(format)
    
    def get_events_dict(self, start_date: datetime, end_date: datetime):
        """Return a dictionary of events from the calendar between the specified dates

        Args:
            start_date (datetime): Start date of events
            end_date (datetime): End date of events
        
        Returns:
            dict: Dictionary of events
        """
        events_list = self.get_events_list(start_date, end_date)

        # convert to dict with keys as uid
        events_dict = {}
        for event in events_list:
            events_dict[event["uid"]] = event
        
        return events_dict
    
    def get_events_list(self, start_date: datetime, end_date: datetime):
        """Return a list of events from the calendar between the specified dates

        Args:
            start_date (datetime): Start date of events
            end_date (datetime): End date of events
        
        Returns:
            list: List of events
        """
        # update the url
        self.url = self.get_url()

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

            event_start = datetime.strptime(str(event.start), "%Y-%m-%d %H:%M:%S%z").replace(tzinfo=pytz.UTC) # get a datetime object of the event starting time
            
            # make sure the timezones are correct
            event_start = event_start.astimezone(tz=self.timezone) # convert to local timezone

            event_start_full = datetime.strftime(event_start, "%c") # make it readable
            event_start_time = datetime.strftime(event_start, "%-I:%M %p") # make it readable

            event_uid = str(event.uid)

            event_timestamp = event_start.timestamp()

            # time until event
            event_time_until = event_start - datetime.now().astimezone(tz=self.timezone)#+timedelta(hours=-12)
            event_time_until_formatted = format_time_until(event_time_until)

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

        return events_list