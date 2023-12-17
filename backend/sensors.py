from pills import PillDatabase
from settings import Settings
from notifications import Notifications

import OPi.GPIO as GPIO
import orangepi.zero3

class Sensors():
    def __init__(self):
        # Set up settings
        self.config = Settings()
        self.config_dict = self.config.get_config_dict()
        self.dispenser_enabled = self.config_dict["dispenser_enabled"]

        # Cancel if dispenser is not in use, technically not necessary because this class is only used by Dispenser
        if not self.dispenser_enabled:
            return
        
        self.pill_database = PillDatabase()
        self.refresh_dispenser_data()

        self.setup_sensors() # safe to do even if no sensors are enabled

    def refresh_dispenser_data(self):
        """Refreshes the dispenser data from the database"""
        self.dispensers = self.pill_database.get_dispensers()

    def setup_sensors(self):
        """Sets up the GPIO for the sensors"""
        self.refresh_dispenser_data()
        # Set up GPIO for the sensors
        GPIO.setmode(orangepi.zero3.BOARD)
        # Get all the pins that need to be inputs
        sensor_pins = []
        for dispenser in self.dispensers:
            if dispenser["sensor_enabled"] == 1:
                sensor_pins.append(dispenser["sensor_pin"])
        # Set them all up as inputs with pull-up resistors
        try:
            GPIO.setup(sensor_pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        except RuntimeError as e:
            print(f"GPIO already set up, raising error: {e}")

    def register_callback(self, dispenser_index, edge, function, debounce):
        """Registers a callback for a dispenser

        Args:
            dispenser_index (int): The index of the dispenser to register the callback for
            edge (s tr): The edge to register the callback for (rising, falling, or both)
            function (function): The function to call when the callback is triggered
            debounce (int): The debounce time in milliseconds
        """
        match edge:
            case "rising":
                trigger = GPIO.RISING
            case "falling":
                trigger = GPIO.FALLING
            case "both":
                trigger = GPIO.BOTH
            case _:
                raise ValueError("Invalid edge type")
        
        GPIO.add_event_detect(self.dispensers[dispenser_index]["sensor_pin"], trigger, callback=function, bouncetime=debounce)

    def unregister_callback(self, dispenser_index):
        """Unregisters a callback for a dispenser

        Args:
            dispenser_index (int): The index of the dispenser to unregister the callback for
        """
        print(f"Removed callback for dispenser {dispenser_index}")
        GPIO.remove_event_detect(self.dispensers[dispenser_index]["sensor_pin"])
