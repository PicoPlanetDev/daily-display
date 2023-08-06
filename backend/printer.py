from Adafruit_Thermal import *
from serial import SerialException

class Printer:
    def __init__(self):
        try:
            self.printer = Adafruit_Thermal("/dev/ttyS5", 9600, timeout=5)
        except SerialException as e:
            print("Printer not found")

    def print_calendar(self, calendar, date):
        self.start()

        # calendar is the dictionary of events
        self.printer.setSize('L')
        self.printer.justify('C')
        self.printer.underlineOn()
        self.printer.println("Calendar")
        self.printer.underlineOff()
        self.printer.setSize('M')
        self.printer.println(date)

        self.printer.setSize('S')
        self.printer.justify('L')
        for event in calendar:
            line = f"{event['start']} - {event['title']})"
            if event['type'] == "Task":
                line = f"[ ] {line}"
            else:
                line = f"    {line}"
            
            self.printer.println(line)

        self.end()
    
    def start(self):
        self.printer.begin(45)

    def end(self):
        self.printer.feed(5)
        self.printer.sleep()
        self.printer.wake()
        self.printer.setDefault()