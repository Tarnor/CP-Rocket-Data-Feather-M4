# CircuitPython for Data Login trials
# Attempting to avoid using CPX Library as that seems to screw some other stuff up
# and this code may be converted to MicroPython anyway....

import time
import board
#import digitalio
#import microcontroller
import neopixel
import random
from digitalio import DigitalInOut, Direction, Pull

RED = (50,0,0)
GREEN = (0,50,0)
BLACK = (0,0,0)
BLUE = (0,0,50)
YELLOW = (50,50,0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.5, auto_write=True)
pixels[0] = RED

filenum = DigitalInOut(board.D5)
filenum.direction = Direction.INPUT
filenum.pull = Pull.UP     #Pull.DOWN apparently means Open Switch = false

filewrite = DigitalInOut(board.D6)
filewrite.direction = Direction.INPUT
filewrite.pull = Pull.UP

def file_name_change():                     #Function to increment FileName on buttonpress
    global file_name

    pixels[0] = YELLOW
    time.sleep(1)
    file_name = "a_" + str(int(time.monotonic()))

file_name = "a_" + str(int(time.monotonic())) + ".txt"
write_file = True


try:
    #with open(file_name, "a") as fp:
        while True:

            pixels[0] = YELLOW
            x = random.random()     #In place of Acceleration
            y = random.random()
            z = random.random()
            t = time.monotonic()

            #fp.write('{:f},{:f},{:f},{:f} \n' .format(t, x, y, z))
            #fp.flush()

            if write_file:
                print(file_name, t, x, y, z)
                print(filenum.value, filewrite.value)

                pixels[0] = GREEN   #Flash Green while writing in loop
                time.sleep(0.5)
                pixels[0] = BLACK
                time.sleep(0.5)
            else:
                pixels[0] = BLUE    #Flash Yellow while writing in loop
                time.sleep(0.5)
                pixels[0] = BLACK
                time.sleep(0.5)


            if not filenum.value:        #If D5 Closed, increment file number
                pixels[0] = YELLOW
                #fp.flush()
                file_name_change()
                time.sleep(2)

            if not filewrite.value:        #If D6 Closed, stop writing
                pixels[0] = BLUE
                #fp.flush()
                write_file = not write_file
                time.sleep(2)


except OSError as e:            #If Can't Write (read Only) then flash RED NeoPixel
    delay = 0.5
    if e.args[0] == 28:
        delay = 0.25
    while True:
        pixels[0] = RED
        time.sleep(delay/2)
        pixels[0] = BLACK
        time.sleep(delay/2)