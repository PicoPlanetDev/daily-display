from icalendar import Calendar, Event
from datetime import datetime
from urllib import request

SECRET_CALENDAR_URL = r"https://calendar.google.com/calendar/ical/945e5e10ca018019d44cfffee2582426f73e74753b798670687c98f3ca8ef243%40group.calendar.google.com/private-1e89336b8a0daa1dcda1fe44530084ba/basic.ics"

ical = request.urlopen(SECRET_CALENDAR_URL).read()
#file = open(SECRET_CALENDAR_URL, 'rb')
calendar = Calendar(ical)

for component in calendar.walk():
    if component.name == "VEVENT":
        summary = component.get("summary")
        description = component.get("description")
        startdt = component.get('dtstart').dt
        enddt = component.get('dtend').dt

        print(f"{startdt.strftime('%c')} to {enddt.strftime('%c')}: {summary}")