#from app import app
from lis2hh12_accel import LIS2HH12
import neopixel
import math

class level:
    accelerometer = None
    pixels = None
    led_divide_angle = [3,6,9,15,19,25,65,130,155]

    def __init__(self, accelorometer: LIS2HH12, pixels: neopixel.NeoPixel, color) -> None:
        self.accelerometer = accelorometer
        self.pixels = pixels
        self.color = color

    def __findIndex(self, Angle):
        found = 100
        last_index = 0
        positive = True
        if Angle < 0:
            positive = False
            Angle *= -1
        for i in range(len(self.led_divide_angle)):
            if Angle < self.led_divide_angle[i]:
                found = i
                break
        if positive:
            return 8 - found
        else:
            return 8 + found
    
    def update(self):
        (x,y,z) = self.accelerometer.acceleration
        XYAngle = (math.atan2(x,y)/math.pi*180)
        index = self.__findIndex(XYAngle)
        self.pixels.fill((0,0,0))
        if index < 0 or index > 16:
            index = 17
        self.pixels[index] = self.color
        print("XY:{0:8.3f}, i:{1:2d}".format(XYAngle, index), end='\r')
    
    def exit(self):
        self.pixels.fill((0,0,0))

    last_led = 0
    def spin(self):
        self.pixels.fill((0,0,0))
        self.pixels[self.last_led] = self.color
        self.last_led += 1
        if self.last_led >= 20:
            self.last_led = 0
