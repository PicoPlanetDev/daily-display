# ensure that the thermal printer module is installed
import os
if not os.path.isfile('Adafruit_Thermal.py'):
    print("Downloading Adafruit Thermal Printer module")
    os.system('wget -O Adafruit_Thermal.py https://raw.githubusercontent.com/adafruit/Python-Thermal-Printer/master/Adafruit_Thermal.py')

from Adafruit_Thermal import *
from serial import SerialException
import settings
import notifications

class Printer:
    def __init__(self):
        self.config = settings.Settings()
        self.config_dict = self.config.get_config_dict()
        self.printer_enabled = self.config_dict["printer_enabled"]
        self.printer_port = self.config_dict["printer_port"]
        self.printer_baudrate = self.config_dict["printer_baudrate"]

        if self.printer_enabled:
            try:
                self.printer = Adafruit_Thermal(self.printer_port, self.printer_baudrate, timeout=5)
            except SerialException as e:
                print("Printer not found")
                # disable printer if it's not found
                self.printer_enabled = False
                self.config.set_key("Printer", "printer_enabled", "false")
                return
        
        self.check_paper()
            
    def check_paper(self):
        if not self.printer_enabled:
            return

        if not self.printer.hasPaper():
            notifications.Notifications().notification("Printer out of paper", "Daily Display", "urgent")

    def print_calendar(self, calendar, date):
        if not self.printer_enabled:
            return

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
            print(event)
            line = f"{event['time_string']} - {event['title']}"
            if event['type'] == "Task":
                line = f"[ ] {line}"
            else:
                line = f"    {line}"
            
            self.printer.println(line)

        self.end()
    
    def start(self):
        self.printer.begin(45)

        self.check_paper()

    def end(self):
        self.printer.feed(5)
        self.printer.sleep()
        self.printer.wake()
        self.printer.setDefault()

    def print_qr(self, qr, link, message):
        if not self.printer_enabled:
            return

        self.start()
        self.printer.justify('C')
        self.printer.setSize('S')
        self.printer.println(message)
        self.printer.println(link)
        self.printer.printImage(qr)
        self.end()