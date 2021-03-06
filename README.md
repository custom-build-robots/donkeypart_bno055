I am building since one year Donkey Cars and now it was time to add an IMU sensor and to develop my first part to get the sensor running.
The picture below shows my Donkey Car without the senors.
To read more about my Donkey Car project just visit my blog: https://custom-build-robots.com/category/donkey_car
![Donkey Car](https://custom-build-robots.com/wp-content/uploads/2018/02/Donkey_Car_01.jpg)

# Custom Donkey Car Part Bosch BNO055 IMU
The BNO055 is the first in a new family of Application Specific Sensor Nodes (ASSN) implementing an intelligent 9-axis Absolute Orientation Sensor, which includes sensors and sensor fusion in a single package.
##  Donkey Car part IMUBNO055
I developed this part to support the BNO055 sensor I used on my Donkey Car. The sensor is connected via UART (RX/TX) and not via I2C. The I2C bus made some problems together with BNO055 sensor which has a slightly different implementation of the I2C bus as the Raspberry Pi supports.
I tested this part with the Dexter Industrial IMU Board shown in the next picture.

![Dexter Industries BNO055 Sensor](https://custom-build-robots.com/wp-content/uploads/2019/03/bno055.jpg)

This part should also work with the Adafruit BNO055 sensor board as well and with cheap clones from China.
## Donkey Car manage.py changes
I had to add the imu part in the manage.py as follows to get the imu values recorded.

The first change was to import the imubno055 part at the end of the "#import parts" section of the manage.py file
...

    # Ingmar Stapel added IMU bno055 201900311
    from donkeycar.parts.imubno055 import bno055

...

The second change was to add the imubno055 part to get the selected sensor values I had choosen.
....

    V.add(cam, outputs=['cam/image_array'], threaded=True)

    # Ingmar Stapel 20190311
    imu = bno055()
    V.add(imu, outputs=['imu/acl_x', 'imu/acl_y', 'imu/acl_z', 'imu/acg_x', 'imu/acg_y', 
    'imu/acg_z', 'imu/gyr_x', 'imu/gyr_y', 'imu/gyr_z', 'imu/temp', 'imu/cali_sys', 
    'imu/cali_gyro', 'imu/cali_accel', 'imu/cali_mag'], threaded=True)  

    if use_joystick or cfg.USE_JOYSTICK_AS_DEFAULT:
...


The third change was the JSON output definition. I added the following lines of code inside the manage.py file.
...

    # add tub to save data
    #inputs = ['cam/image_array', 'user/angle', 'user/throttle', 'user/mode', 'timestamp']
    #types = ['image_array', 'float', 'float',  'str', 'str']

    #Ingmar Stapel 20190311 add tub to save data
    inputs = ['cam/image_array', 'user/angle', 'user/throttle', 'user/mode', 'timestamp',
              'imu/acl_x', 'imu/acl_y', 'imu/acl_z', 'imu/acg_x', 'imu/acg_y', 'imu/acg_z', 
              'imu/gyr_x', 'imu/gyr_y', 'imu/gyr_z', 'imu/temp', 'imu/cali_sys', 'imu/cali_gyro', 
              'imu/cali_accel', 'imu/cali_mag']
    types = ['image_array', 'float', 'float',  'str', 'str', 'float', 'float', 'float', 'float', 
             'float', 'float', 'float', 'float', 'float', 'float', 'int', 'int', 'int', 'int']
 ...
 
 Now, the Donkey Car framework should work together with the BNO055 sensor. The values of the BNO055 sensor where recorded in the JSON files.
