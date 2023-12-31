from PCA9685_smbus2 import PCA9685
import time
from settings import Settings
from pills import PillDatabase
from notifications import Notifications
from sensors import Sensors

# True limits seem to be 86 to 535
# SERVO_MIN = 100
# SERVO_MAX = 500

# SERVO_DEFAULT = 90
# SERVO_CHUTE = 0

def map_range(value, inMin, inMax, outMin, outMax):
    """Maps a value from one range to another using linear interpolation without clamping

    Args:
        value: The value to map
        inMin: The minimum value of the input range
        inMax: The maximum value of the input range
        outMin: The minimum value of the output range
        outMax: The maximum value of the output range

    Returns:
        _type_: _description_
    """        
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

class Dispenser:
    def __init__(self, i2c_bus: int, i2c_address: int):
        """Initializes the dispenser motor driver (if enabled) and sets up the sensors

        Args:
            i2c_bus (int): The I2C bus that the PCA9685 is connected to
            i2c_address (int): The I2C address of the PCA9685
        """
        # Set up settings
        self.config = Settings()
        self.config_dict = self.config.get_config_dict()
        self.dispenser_enabled = self.config_dict["dispenser_enabled"]
        # Cancel if dispenser is not in use
        if not self.dispenser_enabled:
            return

        # Set up the sensors
        self.sensors = Sensors()

        # Get info about the dispensers
        self.pill_database = PillDatabase()
        self.refresh_dispenser_data()

        # Be able to send notifications
        self.notifications = Notifications()

        # Actually set up the servo driver
        self.pwm = PCA9685.PCA9685(i2c_bus, i2c_address)
        self.pwm.set_pwm_freq(50) # SG90 servos use a 50Hz PWM signal

    def refresh_dispenser_data(self):
        """Refreshes the dispenser data from the database"""
        self.dispensers = self.pill_database.get_dispensers()
        self.sensors.setup_sensors()

    def set_servo_angle(self, servo_channel: int, angle):
        """Sets the angle of a servo motor connected to the PCA9685

        Args:
            servo_channel (int): The channel, from 0 to 15, of the servo motor on the PCA9685
            angle: The angle to set the servo motor to, from 0 to 180
        """
        if not self.dispenser_enabled:
            return
        
        servo_min = self.dispensers[servo_channel]["servo_min"]
        servo_max = self.dispensers[servo_channel]["servo_max"]

        pulse = int(map_range(angle, 0, 180, servo_min, servo_max))
        self.pwm.set_pwm(servo_channel, 0, pulse)

    def smooth_angle_change(self, servo_channel: int, angle_start, angle_end):
        """Interpolates between two angles to smoothly change the angle of a servo motor
        
        Args:
            servo_channel (int): The channel, from 0 to 15, of the servo motor on the PCA9685
            angle_start: The angle to start the interpolation at, from 0 to 180
            angle_end: The angle to end the interpolation at, from 0 to 180
        """
        duration = self.dispensers[servo_channel]["smooth_duration"]
        step_time = self.dispensers[servo_channel]["step_time"]
        steps = int(duration / step_time)
        self.set_servo_angle(servo_channel, angle_start)
        for i in range(steps):
                interpolated = map_range(i/steps, 0,1,angle_start,angle_end)
                self.set_servo_angle(servo_channel, interpolated)
                time.sleep(step_time)
        self.set_servo_angle(servo_channel,angle_end)

    def dispense_pill(self, dispenser_index, number_of_pills=1):
        """Dispenses a pill from the dispenser, optionally repeatedly

        Args:
            dispenser_index (int): The index of the dispenser to run
            number_of_pills (int): The number of pills to dispense
        """        
        if not self.dispenser_enabled:
            return

        self.sensors.register_callback(dispenser_index, "falling", self.dispense_pill_callback, 500) # register the callback for when the pill is dispensed

        for i in range(number_of_pills):
            self.cycle_dispenser(dispenser_index) # dispense as many pills as needed

    def dispense_pill_callback(self, sensor_pin):
        """Callback for when a pill is dispensed from a dispenser

        Args:
            sensor_pin (int): The index of the dispenser that triggered the callback
        """        
        if not self.dispenser_enabled:
            return
        
        print(f"callback on {sensor_pin}")
        # self.notifications.notification(f"Callback from sensor on pin {sensor_pin}", "Daily Display", "default")

        # determine which dispenser was triggered
        dispenser_index = None
        for dispenser in self.dispensers:
            if dispenser["sensor_pin"] == sensor_pin:
                dispenser_index = dispenser["index"]
                break
        # self.notifications.notification(f"Pill dispensed from dispenser {dispenser_index}", "Daily Display", "default")
        self.pill_database.set_pill_dispensed(dispenser_index)

        # Figure out the pill that was dispensed
        pill = self.pill_database.get_pill(dispenser_index)
        self.notifications.notification(f"{pill['name']} dispensed", title="Pill dispensed", priority="default", tags="pill")

        self.sensors.unregister_callback(dispenser_index)
        
    #     self.sensors.register_callback(dispenser_index, "both", self.take_pill_callback, 500)

    # def take_pill_callback(self, sensor_pin):
    #     """Callback for when a hand removes a pill from a dispenser

    #     Args:
    #         sensor_pin (int): The index of the dispenser that triggered the callback
    #     """          
    #     if not self.dispenser_enabled:
    #         return
        
    #     print(f"callback on {sensor_pin}")
        
    #     # determine which dispenser was triggered
    #     dispenser_index = None
    #     for dispenser in self.dispensers:
    #         if dispenser["sensor_pin"] == sensor_pin:
    #             dispenser_index = dispenser["index"]
    #             break

    #     # Figure out the pill that was dispensed
    #     pill = self.pill_database.get_pill(dispenser_index)
    #     self.notifications.notification(f"{pill['name']} taken", title="Pill taken", priority="default", tags="pill")

    #     self.sensors.unregister_callback(dispenser_index)

    def reset_dispenser(self, dispenser_index):
        """Resets the dispenser to the default angle

        Args:
            dispenser_index (int): The index of the dispenser to reset
        """
        if not self.dispenser_enabled:
            return
        
        angle_default = self.dispensers[dispenser_index]["angle_default"] # get the angle to reset to
        self.set_servo_angle(dispenser_index, angle_default) # rotate the servo

    def cycle_dispenser(self, dispenser_index):
        """Cycles the dispenser to the chute angle and back to the default angle

        Args:
            dispenser_index (int): The index of the dispenser to cycle
        """        
        if not self.dispenser_enabled:
            return
        
        # self.notifications.notification(f"Cycling dispenser {dispenser_index}", "Daily Display", "default", "gear")
        
        # self.sensors.register_callback(dispenser_index, "falling", self.dispense_pill_callback, 500) # register the callback for when the pill is dispensed

        angle_default = self.dispensers[dispenser_index]["angle_default"] # the servo's angle when aligned with the hopper
        angle_chute = self.dispensers[dispenser_index]["angle_chute"] # the servo's angle when aligned with the chute

        smooth_enabled = True if self.dispensers[dispenser_index]["smooth_enabled"] == 1 else False # figure out if we should use smooth angle change or not
        if smooth_enabled:
            self.smooth_angle_change(dispenser_index, angle_default, angle_chute) # dispense, starting from default angle
            time.sleep(0.5)
            self.smooth_angle_change(dispenser_index, angle_chute, angle_default) # return, starting from chute angle
            time.sleep(0.5)
        else:
            self.set_servo_angle(dispenser_index, angle_default) # reset to default just in case
            time.sleep(0.5)
            self.set_servo_angle(dispenser_index, angle_chute) # dispense
            time.sleep(0.5)
            self.set_servo_angle(dispenser_index, angle_default) # return
            time.sleep(0.5)