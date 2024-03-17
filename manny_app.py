# from app import app
from lis2hh12_accel import LIS2HH12
from display import Display
import neopixel
import math
import time
from app_base import AppBase


class manny(AppBase):
    accelerometer = None
    display = None
    pixels = None
    prevx = 0
    prevy = 0
    rectsize = 2

    def __init__(
        self, accelorometer: LIS2HH12, display: Display, pixels: neopixel.NeoPixel
    ) -> None:
        self.accelerometer = accelorometer
        self.pixels = pixels
        self.display = display
        self.display.clear()

    def update(self, dt: float):
        self.drawrect(20,20)
        now = time.monotonic()
        (x, y, z) = self.accelerometer.acceleration
        xdif = self.prevx - x
        ydif = self.prevy - y
        print("X:{0:8.3f}, Y:{1:8.3f}, xdif:{2:8.3f}, ydif:{3:8.3f}".format(x, y, xdif, ydif), end="\r")

    def exit(self):
        self.pixels.fill((0, 0, 0))

    def drawrect(self, x, y):
        self.display.get().fill_rect(x,y,self.rectsize,self.rectsize,1)
        self.display.get().show()
