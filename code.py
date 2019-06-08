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
import neopixel

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

#Set Up NeoPixel on Feather
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3

# Subroutines ========================================================================
# Get a new Log Filename which is an increment of existing files in the directory
def get_log_filename():
    i=0
    log_fn = "log" + str(int(i)) +".csv"
    while log_fn in os.listdir("/sd"):
        i +=1
        log_fn = "log" + str(int(i)) +".csv"
    return log_fn
    
def write_oled():
    oled.fill(0)
    if not logging_paused:
        oled.text('Logging to file',0,0,1)
        led[0] = (0, 255, 0)               #LED to GREEN
    else:
        oled.text('Logging PAUSED',0,0,1)
        led[0] = (255, 255, 0)
    oled.text(logfn,0,10,1)
    oled.show()    

def logphysics():
    global logging_paused
    while True:    
        try:
            with open("/sd/"+logfn,"a") as fp:
                #Poll Sensors
                accel_x, accel_y, accel_z = sensor.acceleration
                mag_x, mag_y, mag_z = sensor.magnetic
                gyro_x, gyro_y, gyro_z = sensor.gyro
                temp = sensor.temperature
                altitude = bme280.altitude
                t = time.monotonic()

                #time.sleep(0.25)

                if not button1.value:       #Return Normal on Button Push
                    fp.flush
                    logging_paused = True
                    write_oled()
                    return -10

                if not logging_paused:
                    fp.write('{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f},{:f} \n' .format(t,accel_x,accel_y,accel_z, gyro_x,gyro_y,gyro_z, mag_x, mag_y, mag_z,temp,altitude))
                    print(t)
        except OSError as e:            #If Can't Write (read Only) then flash RED NeoPixel on PIXEL 1
            #pixels[1] = WHITE
            #if e.args[0] == 28:         #Error 28 flashes WHITE
            #    pixels[0] = WHITE
            print("ERROR WRITING FILE")
            return -99
            #else:                       #Can't write to storage, so print to serial
            #    print("Can't write to File: " + log_fn)
            #    print(log_fn + " " + '{:f},{:f},{:f},{:f}' .format(t, x, y, z))
            #    print(buttonA.value, buttonB.value, switchA.value)
            #    pixels[0] = RED
            #    return -99


# Main Routine ========================================================================

# Run Once ===============


logfn = get_log_filename()          #Get first unused filename spot
led[0] = (255,255,0)                #Yellow LED to start
logging_paused = True               #Start with Logging to SD Card Paused
write_oled()
time.sleep(1)                       #Hold for One Second

#Main Loop ===============
while True:
    #Display text if Button Held Down 5,6,9
    print(logging_paused, logfn, button1.value, button2.value, button3.value,"\n")
    time.sleep(0.1)
    
    if not button1.value:                       #If Button1 Pushed
        logging_paused = not logging_paused
        if logging_paused:
            write_oled()
        else:
            write_oled()
            returnphysics = logphysics()
        time.sleep(0.15)
    if not button2.value:                       #If Button2 Pushed
        logging_paused = True
        logfn = get_log_filename()          #Get first unused filename spot
        write_oled()
        time.sleep(0.15)
