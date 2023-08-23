from icalevents import icalevents
from datetime import datetime, timedelta

SECRET_ICAL_URL = r"https://calendar.google.com/calendar/ical/945e5e10ca018019d44cfffee2582426f73e74753b798670687c98f3ca8ef243%40group.calendar.google.com/private-1e89336b8a0daa1dcda1fe44530084ba/basic.ics"

today = datetime.today()
start_date = today
end_date=today+timedelta(days=2)
events_list = icalevents.events(SECRET_ICAL_URL, start=start_date, end=end_date)

for event in events_list:
    event_title = str(event.summary) # with the LABELS

    prefix = ""
    if "TASK" in event_title:
        prefix = "(TASK)"

    title_friendly = event_title.replace("TASK", "").strip() # no labels, no leading/trailing white

    event_start = datetime.strptime(str(event.start), "%Y-%m-%d %H:%M:%S%z") # get a datetime object of the event starting time
    event_start_friendly = datetime.strftime(event_start, "%c") # make it readable

    description = f"{prefix} {event_start_friendly} - {title_friendly}"

    print(description)

# event.summary - the title
# event.description - the description

