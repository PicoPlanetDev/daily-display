import configparser

class Settings():
    def __init__(self, path='config.ini'):
        self.path = path
        self.config = configparser.ConfigParser(interpolation=None, allow_no_value=True)
        # If config file exists, read it
        if self.config.read(path):
            print("Config file found")
        # Else, create it
        else:
            print("Config file not found")
            self.create_config()

    def create_config(self):
        """
        Create a config file
        """
        self.config.add_section("Notifications")
        self.config.set("Notifications", "notification_url", "https://ntfy.sh/mytopic")
        self.config.set("Notifications", "notifications_enabled", "true")

        self.config.add_section("Calendar")
        self.config.set("Calendar", "calendar_url", "https://linktoicsfile.ics")
        self.config.set("Calendar", "timezone", "America/New_York")

        self.config.add_section("Printer")
        self.config.set("Printer", "printer_enabled", "true")
        self.config.set("Printer", "printer_port", "/dev/ttyS5")
        self.config.set("Printer", "printer_baudrate", "9600")
        self.config.set("Printer", "receipt_rounds", "")

        self.config.add_section("Dispenser")
        self.config.set("Dispenser", "dispenser_enabled", "true")
        self.config.set("Dispenser", "manual_dispense_time", "60")

        self.config.add_section("Kiosk")
        self.config.set("Kiosk", "kiosk_enabled", "true")
        
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def get_config_dict(self):
        """
        Return config as a dictionary
        """
        return {
            "notification_url": self.config.get("Notifications", "notification_url"),
            "notifications_enabled": self.config.getboolean("Notifications", "notifications_enabled"),
            "calendar_url": self.config.get("Calendar", "calendar_url"),
            "timezone": self.config.get("Calendar", "timezone"),
            "printer_enabled": self.config.getboolean("Printer", "printer_enabled"),
            "printer_port": self.config.get("Printer", "printer_port"),
            "printer_baudrate": self.config.getint("Printer", "printer_baudrate"),
            "dispenser_enabled": self.config.getboolean("Dispenser", "dispenser_enabled"),
            "receipt_rounds": self.config.get("Printer", "receipt_rounds"),
            "manual_dispense": self.config.getint("Dispenser", "manual_dispense_time"),
            "kiosk_enabled": self.config.getboolean("Kiosk", "kiosk_enabled")
        }
    
    def update_config(self, dictionary):
        """
        Update config with dictionary
        """
        try:
            self.config.set("Notifications", "notification_url", dictionary["notification_url"])
            self.config.set("Notifications", "notifications_enabled", "true" if dictionary["notifications_enabled"] else "false")
            self.config.set("Calendar", "calendar_url", dictionary["calendar_url"])
            self.config.set("Calendar", "timezone", dictionary["timezone"])
            self.config.set("Printer", "printer_enabled", "true" if dictionary["printer_enabled"] else "false")
            self.config.set("Printer", "printer_port", dictionary["printer_port"])
            self.config.set("Printer", "printer_baudrate", str(dictionary["printer_baudrate"]))
            self.config.set("Dispenser", "dispenser_enabled", "true" if dictionary["dispenser_enabled"] else "false")
            self.config.set("Printer", "receipt_rounds", dictionary["receipt_rounds"])
            self.config.set("Dispenser", "manual_dispense_time", str(dictionary["manual_dispense"]))
            self.config.set("Kiosk", "kiosk_enabled", "true" if dictionary["kiosk_enabled"] else "false")
        except KeyError as e:
            print("KeyError: {}".format(e))
            return False

        with open(self.path, 'w') as configfile:
            self.config.write(configfile)
        
        return True
    
    def set_key(self, section, key, value):
        self.config.set(section, key, value)
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)