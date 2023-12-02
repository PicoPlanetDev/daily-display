from PCA9685_smbus2 import PCA9685
import time
import settings

# True limits seem to be 86 to 535
SERVO_MIN = 100
SERVO_MAX = 500

SERVO_DEFAULT = 90
SERVO_CHUTE = 0

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
    def __init__(self, i2c_bus, i2c_address):
        self.config = settings.Settings()
        self.config_dict = self.config.get_config_dict()
        self.dispenser_enabled = self.config_dict["dispenser_enabled"]
        if not self.dispenser_enabled:
            return
        
        self.pwm = PCA9685.PCA9685(i2c_bus, i2c_address)
        self.pwm.set_pwm_freq(50) # 50 Hz drives SG90 servo motors well

    def set_servo_angle(self, servo_channel: int, angle):
        """Sets the angle of a servo motor connected to the PCA9685

        Args:
            servo_channel (int): The channel, from 0 to 15, of the servo motor on the PCA9685
            angle: The angle to set the servo motor to, from 0 to 180
        """
        if not self.dispenser_enabled:
            return
        
        pulse = int(map_range(angle, 0, 180, SERVO_MIN, SERVO_MAX))
        self.pwm.set_pwm(servo_channel, 0, pulse)

    def dispense_pill(self, dispenser_index, number_of_pills=1):
        """Dispenses a pill from the dispenser, optionally repeatedly

        Args:
            dispenser_index (int): The index of the dispenser to run
            number_of_pills (int): The number of pills to dispense
        """        
        if not self.dispenser_enabled:
            return

        for i in range(number_of_pills):
            self.cycle_dispenser(dispenser_index)

    def reset_dispenser(self, dispenser_index):
        """Resets the dispenser to the 0 degree position (closed)

        Args:
            dispenser_index (int): The index of the dispenser to reset
        """
        if not self.dispenser_enabled:
            return
            
        self.set_servo_angle(dispenser_index, SERVO_DEFAULT)

    def cycle_dispenser(self, dispenser_index):
        """Cycles the dispenser to the 90 degree position (open) and back to the 0 degree position (closed)

        Args:
            dispenser_index (int): The index of the dispenser to cycle
        """        
        if not self.dispenser_enabled:
            return

        self.set_servo_angle(dispenser_index, SERVO_DEFAULT)
        time.sleep(1)
        self.set_servo_angle(dispenser_index, SERVO_CHUTE)
        time.sleep(1)
        self.set_servo_angle(dispenser_index, SERVO_DEFAULT)
        time.sleep(1)