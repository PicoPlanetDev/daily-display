from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import settings
import os

# Creates a chromium kiosk window to display the web interface
class Kiosk():
    def __init__(self):
        self.config = settings.Settings()
        self.config_dict = self.config.get_config_dict()
        self.kiosk_enabled = self.config_dict["kiosk_enabled"]
        if self.kiosk_enabled:
            self.start()

    def start(self):
        chrome_options = Options()
        chrome_options.add_argument("--kiosk")
        chrome_service = webdriver.ChromeService(executable_path='chromedriver')

        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.driver.get("http://localhost:5173")

    def stop(self):
        self.driver.quit()