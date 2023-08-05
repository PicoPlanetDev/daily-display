import requests
import settings

class Notifications:
    def __init__(self):
        self.refresh_config()
    
    def refresh_config(self):
        config = settings.Settings()
        config_dict = config.get_config_dict()
        self.url = config_dict["notification_url"]
        self.notifications_enabled = config_dict["notifications_enabled"]

    def notification(self, message, title="Daily Display", priority="default", tags=""):
        """
        Send a notification to the notification server.
        
        Args:
            message (str): The message to send.
            title (str): The title of the notification.
            priority (str): The priority of the notification. Can be "min", "low", "default", "high", "urgent".
            tags (str): A comma-separated list of emojis to send with the notification.
        
        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        self.refresh_config()
        if not self.notifications_enabled:
            return False
        requests.post(self.url, 
                        data=message.encode(encoding='utf-8'),
                        headers={
                                "Title": title,
                                "Priority": priority,
                                "Tags": tags})
        return True
