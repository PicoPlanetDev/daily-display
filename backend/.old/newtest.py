from icalevents.icalevents import events
from datetime import datetime, timedelta
import pytz

url = r"https://calendar.google.com/calendar/ical/945e5e10ca018019d44cfffee2582426f73e74753b798670687c98f3ca8ef243%40group.calendar.google.com/private-1e89336b8a0daa1dcda1fe44530084ba/basic.ics"

#Start and End need to be in UTC, see PR #108
my_timezone = pytz.timezone('Australia/Melbourne')
now = datetime.now().astimezone(pytz.timezone('UTC'))
future = (now + timedelta(hours=200)).astimezone(pytz.timezone('UTC'))

es = events(url, start=now, end=future)

#Return start date from event
def get_start(event):
    return event.start.astimezone(my_timezone)

#Sort events earliest to latest
es.sort(key=get_start)

#Move through each event and print something about it to terminal
for e in es:
    e.start = e.start.astimezone(my_timezone)
    e.end = e.end.astimezone(my_timezone)
    print(e.start.strftime("%Y-%m-%d %H:%M") + ' to ' + e.end.strftime("%Y-%m-%d %H:%M") + ' ' + e.summary )
   #You can see all of the object properties in icalparser.py - e.g. uid, summary description, start, end...