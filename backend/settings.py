import configparser

class Settings():
    def __init__(self, path='config.ini'):
        self.path = path
        self.config = configparser.ConfigParser()
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
        config = configparser.ConfigParser()
        config.add_section("Notifications")
        config.set("Notifications", "notification_url", "https://ntfy.sh/mytopic")
        config.set("Notifications", "notifications_enabled", "true")
        
        with open(self.path, "w") as config_file:
            config.write(config_file)

    def get_config_dict(self):
        """
        Return config as a dictionary
        """
        return {
            "notification_url": self.config.get("Notifications", "notification_url"),
            "notifications_enabled": self.config.get("Notifications", "notifications_enabled")
        }
    
    def update_config(self, dictionary):
        """
        Update config with dictionary
        """
        try:
            self.config.set("Notifications", "notification_url", dictionary["notification_url"])
            self.config.set("Notifications", "notifications_enabled", "true" if dictionary["notifications_enabled"] else "false")
        except KeyError as e:
            print("KeyError: {}".format(e))
            return False


        with open(self.path, 'w') as configfile:
            self.config.write(configfile)
        
        return True