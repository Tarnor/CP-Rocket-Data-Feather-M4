# Feather M4 with external Featherwing Adalogger and sensor boards



import board                            #Board Library
import adafruit_lis3dh                  #accelerometer
import time                             #time calculations
import digitalio                        #Digital Input and Output for board
import random                           #Used to create data for output if sensor not connected
import neopixel                         #NeoPixel Ring 10 pixels on Playground
import os
import busio
import adafruit_ssd1306
import adafruit_sdcard
import storage
import adafruit_lsm9ds1
import adafruit_bme280

from digitalio import DigitalInOut, Direction, Pull

# Hardware I2C setup on CircuitPlayground Express for Accelerometer:
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# SD Card Setup
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D10)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Accelerometer / Barometer Setup
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
sensor.accel_range = adafruit_lsm9ds1.ACCELRANGE_8G
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

#Define and Set up 3 Buttons on OLED display
button1 = DigitalInOut(board.D9)
button1.direction = Direction.INPUT
button1.pull = Pull.UP
button2 = DigitalInOut(board.D6)
button2.direction = Direction.INPUT
button2.pull = Pull.UP
button3 = DigitalInOut(board.D5)
button3.direction = Direction.INPUT
button3.pull = Pull.UP


# int1 = digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT)
# lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)
# lis3dh.range = adafruit_lis3dh.RANGE_8_G

import neopixel
led = neopixel.NeoPixel(board.NEOPIXEL, 1)

led.brightness = 0.3

while True:
    #Display text if Button Held Down 5,6,9
    print(button1.value, button2.value, button3.value,"\n")
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temp = sensor.temperature
    altitude = bme280.altitude
    print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
    print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
    print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
    print('Temperature: {0:0.3f}C'.format(temp))
    print('Altitude: {0:0.3f}m'.format(altitude))
    
    if not button1.value:
        led[0] = (0, 255, 0)
        oled.fill(0)
        oled.text('Button 1 Pushed',0,0,1)
        oled.show()
        with open("/sd/test.txt", "w") as f:
            f.write("Hello world!\r\n")
    elif not button2.value:
        led[0] = (255, 0, 0)
        oled.fill(0)
        oled.text('Button 2 Pushed',0,0,1)
        oled.show()
    elif not button3.value:
        led[0] = (0, 0, 255)
        oled.fill(0)
        oled.text('Button 3 Pushed',0,0,1)
        oled.show()
    else:
        led[0] = (255,255,0)
        oled.fill(0)
        oled.show()
    