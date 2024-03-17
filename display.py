import adafruit_ssd1306
from busio import I2C

class Display:
    def __init__(self, i2c: I2C) -> None:
        # Create a display object with 128x32 resolution and an I2C address of 0x3C
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

    def printLine(self, text, line):
        y = 0
        y = (line * 10) - 10
        self.display.fill_rect(0,y,128,10,0)
        self.display.text(text, 0, y, 1)
        self.display.show()
    
    def clear(self):
        self.display.fill(0)
        self.display.show()

    def get(self):
        return self.display
