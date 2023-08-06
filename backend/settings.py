import configparser

class Settings():
    def __init__(self, path='config.ini'):
        self.path = path
        self.config = configparser.ConfigParser(interpolation=None)
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
        self.config.set("Calendar", "calendar_url", "https://linktoicsfile")
        
        with open(self.path, "w") as config_file:
            self.config.write(config_file)

    def get_config_dict(self):
        """
        Return config as a dictionary
        """
        return {
            "notification_url": self.config.get("Notifications", "notification_url"),
            "notifications_enabled": self.config.getboolean("Notifications", "notifications_enabled"),
            "calendar_url": self.config.get("Calendar", "calendar_url")
        }
    
    def update_config(self, dictionary):
        """
        Update config with dictionary
        """
        try:
            self.config.set("Notifications", "notification_url", dictionary["notification_url"])
            self.config.set("Notifications", "notifications_enabled", "true" if dictionary["notifications_enabled"] else "false")
            self.config.set("Calendar", "calendar_url", dictionary["calendar_url"])
        except KeyError as e:
            print("KeyError: {}".format(e))
            return False


        with open(self.path, 'w') as configfile:
            self.config.write(configfile)
        
        return True