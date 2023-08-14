from PCA9685_smbus2 import PCA9685
import time
import settings

# True limits seem to be 86 to 535
SERVO_MIN = 100
SERVO_MAX = 500

def map_range(value, inMin, inMax, outMin, outMax):
        return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

class Dispenser:
    def __init__(self, i2c_bus, i2c_address):
        self.config = settings.Settings()
        self.config_dict = self.config.get_config_dict()
        self.dispenser_enabled = self.config_dict["dispenser_enabled"]
        if not self.dispenser_enabled:
            return
        
        self.pwm = PCA9685.PCA9685(i2c_bus, i2c_address)
        self.pwm.set_pwm_freq(50)

    def set_servo_angle(self, servo_channel, angle):
        if not self.dispenser_enabled:
            return
        
        pulse = map_range(angle, 0, 180, SERVO_MIN, SERVO_MAX)
        self.pwm.set_pwm(servo_channel, 0, pulse)

    def dispense_pill(self, dispenser_index, number_of_pills):
        if not self.dispenser_enabled:
            return

        for i in range(number_of_pills):
            self.set_servo_angle(dispenser_index, 0)
            time.sleep(1)
            self.set_servo_angle(dispenser_index, 90)
            time.sleep(1)
            self.set_servo_angle(dispenser_index, 0)
            time.sleep(1)