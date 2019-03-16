# Autor: Ingmar Stapel
# Homepage: www.custom-build-robots.com
# Date: 20190311
# This part is used to read the BNO055 data.
    # Linear Acceleration Vector
    # Gravity Vector
    # Gyro
    # Calibration information
    # ....
import sys
import time

from Adafruit_BNO055 import BNO055

class bno055:
    """
    Adafruit 9-DOF Absolute Orientation IMU Fusion Breakout - BNO055 
    https://www.adafruit.com/product/2472

    Installation:
    please visit the Adafruit product website or follow the link below
    to read more about the BNO055 sensor and how to install the software.
    https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black

    Short BNO055 installation description:
        cd ~
        git clone https://github.com/adafruit/Adafruit_Python_BNO055.git
        cd Adafruit_Python_BNO055
        You have to install the BNO055 for Phton3.
        sudo python3 setup.py install

    You have to install RPi for Python3.
    sudo apt-get install python-rpi.gpio python3-rpi.gpio

    ToDo:
    - Discuss the the need to save/load the calibration data of the BNO055 sensor
      - BNO055 save calibration
      - BNO055 load calibration
    """

    def __init__(self, poll_delay=0.0166):
        # Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
        self.bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
        self.self_test()  
        self.accel_linear = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.accel_gravity = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.gyro = { 'x' : 0., 'y' : 0., 'z' : 0. }
        self.calibration = { 'sys' : 0., 'gyro' : 0., 'accel' : 0, 'mag' : 0. }
        self.temp = 0.
        self.poll_delay = poll_delay
        self.on = True

    def update(self):
        while self.on:
            self.poll()
            time.sleep(self.poll_delay)

    # Actual no end to end implementation for generating, saving and loadingof the calibration
    # is planned. The BNOO055 sensor calibrates itself constantly when powered up...
    #def load_calibration(self):
    #    # The calibration information for the BNO055 is stored in JSON format.
    #    # To generate and save the calibration information please use the Adafruit
    #    # web-example. 
    #    CALIBRATION_FILE = 'calibration.json'    
    #
    #    # Load calibration from disk.
    #    with open(CALIBRATION_FILE, 'r') as cal_file:
    #        data = json.load(cal_file)
    #    # Grab the lock on BNO sensor access to serial access to the sensor.
    #    with bno_changed:
    #        bno.set_calibration(data)
    #    return 'OK'


    def poll(self):
        # Linear acceleration data (i.e. acceleration from movement, not gravity--
        # returned in meters per second squared):        
        self.accel_linear = self.bno.read_linear_acceleration()
        # Gravity acceleration data (i.e. acceleration just from gravity--returned
        # in meters per second squared):        
        self.accel_gravity = self.bno.read_gravity()
        # Gyroscope data (in degrees per second):        
        self.gyro = self.bno.read_gyroscope()
        # Sensor temperature in degrees Celsius:        
        self.temp = self.bno.read_temp()

        # Other values you can optionally read:
        # Orientation as a quaternion:
        #x,y,z,w = bno.read_quaterion()
        # Magnetometer data (in micro-Teslas):
        #x,y,z = bno.read_magnetometer()
        # Gyroscope data (in degrees per second):
        #x,y,z = bno.read_gyroscope()
        # Accelerometer data (in meters per second squared):
        #x,y,z = bno.read_accelerometer()
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        #heading, roll, pitch = bno.read_euler()
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        #sys, gyro, accel, mag = bno.get_calibration_status()
        self.calibration = self.bno.get_calibration_status()

    def run_threaded(self):
        return self.accel_linear[0], self.accel_linear[1], self.accel_linear[2], self.accel_gravity[0], self.accel_gravity[1], self.accel_gravity[2], self.gyro[0], self.gyro[1], self.gyro[2], self.temp, self.calibration[0], self.calibration[1], self.calibration[2], self.calibration[3]
    def run(self):
        self.poll()
        return self.accel_linear[0], self.accel_linear[1], self.accel_linear[2], self.accel_gravity[0], self.accel_gravity[1], self.accel_gravity[2], self.gyro[0], self.gyro[1], self.gyro[2], self.temp, self.calibration[0], self.calibration[1], self.calibration[2], self.calibration[3]
    def self_test(self):
        # Initialize the BNO055 and stop if something went wrong.
        if not self.bno.begin():
            raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?') 

        # Print system status and self test result.
        status, self_test, error = self.bno.get_system_status()
        print('System status: {0}'.format(status))
        print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
        # Print out an error if system status is in error mode.
        if status == 0x01:
            print('System error: {0}'.format(error))
            print('See datasheet section 4.3.59 for the meaning.')       

    def shutdown(self):
        self.on = False


if __name__ == "__main__":
    print("lets drive...")
