from board import *
from busio import I2C
import busio
import adafruit_ssd1306

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
printLine('J&M', 1)
printLine('4EVA', 2)

count = 0
while True:
    printLine(f's:{count}', 3)
    time.sleep(1)
    count += 1