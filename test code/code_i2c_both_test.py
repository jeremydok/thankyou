from board import *
from busio import I2C
import busio
import adafruit_ssd1306
import digitalio
import time
from lis2hh12_accel import LIS2HH12

def printLine(text, line):
    y = 0
    y = (line * 10) - 10
    display.fill_rect(0,y,128,10,0)
    display.text(text, 0, y, 1)
    display.show()

# Initialize I2C communication using IO6 and IO5 pins
i2c = I2C(IO6,IO5)

# Create a display object with 128x64 resolution and an I2C address of 0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

# Clear the display
display.fill(0)
display.show()

# Write text on the display
printLine('JM4EVA', 1)

device = LIS2HH12(i2c)
print(hex(device.whoami))

upSwitch = digitalio.DigitalInOut(IO1)
upSwitch.direction = digitalio.Direction.INPUT
upSwitch.pull = digitalio.Pull.UP

rightSwitch = digitalio.DigitalInOut(IO2)
rightSwitch.direction = digitalio.Direction.INPUT
rightSwitch.pull = digitalio.Pull.UP

downSwitch = digitalio.DigitalInOut(IO3)
downSwitch.direction = digitalio.Direction.INPUT
downSwitch.pull = digitalio.Pull.UP

leftSwitch = digitalio.DigitalInOut(IO9)
leftSwitch.direction = digitalio.Direction.INPUT
leftSwitch.pull = digitalio.Pull.UP

printLine('Buttons ready', 2)
time.sleep(0.5)

while True:
    if not upSwitch.value:
        printLine('Up', 2)
    if not rightSwitch.value:
        printLine('B', 2)
    if not downSwitch.value:
        printLine('Down', 2)
    if not leftSwitch.value:
        printLine('A', 2)
    print(device.acceleration)
    time.sleep(0.5)