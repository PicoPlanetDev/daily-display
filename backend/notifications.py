import requests
import settings

class Notifications:
    def __init__(self):
        self.config = settings.Settings()
        self.refresh_config()
    
    def refresh_config(self):
        self.url = self.config.get_config_dict()["notification_url"]
        self.notifications_enabled = self.config.get_config_dict()["notifications_enabled"]

    def notification(self, message, title="Daily Display", priority="default", tags=""):
        self.refresh_config()
        if self.notifications_enabled:
            requests.post(self.url, 
                          data=message.encode(encoding='utf-8'),
                          headers={"Title": title,
                                   "Priority": priority,
                                   "Tags": tags},
                          )