from board import *
from busio import I2C
import busio
import espidf

import time
import array
import math

import os
import digitalio
import asyncio

import neopixel

import audiocore
import audiobusio

from lis2hh12_accel import LIS2HH12
from wifi_code import thankyou_wifi
from buttons import Buttons
from display import Display

from level_app import level
from player import Player
from net_app import netGet

#Disable wifi so it has time to restart
useWifi = os.getenv('USE_WIFI') == "True"
wifi = None
if useWifi:
    wifi = thankyou_wifi()

# Initialize I2C communication using IO6 and IO5 pins
i2c = I2C(IO6,IO5)

# Initialize the Display
display = Display(i2c)

# Clear the display
display.get().fill(0)
display.get().show()
display.printLine('J&M 4EVA', 1)

# Setup Accelerometer
device = LIS2HH12(i2c)
display.printLine('Accelerometer ready', 2)

# Setup NeoPixels
pixel_pin = IO4
num_pixels = 20
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=True)
pixels.fill((0,0,0))
pixels.show()
display.printLine('Pixels ready', 2)

# Setup buttons
buttons = Buttons()
display.printLine('Buttons ready', 2)

# Setup audio
audio = audiobusio.I2SOut(IO44, IO7, IO8)
display.printLine('Audio ready', 2)

#blue_level = level(device, pixels)
apps = [("Level Red", level(device, pixels, (64,0,0))),
        ("Level Green", level(device, pixels, (0,64,0))),
        ("Level Blue", level(device, pixels, (0,0,64))),
        ("Play 2001", Player(audio, buttons, display)),
        ("Network", netGet(wifi, buttons, display)),
        ]
app_index = 0
running = False

display.clear()
display.printLine("Select an app", 1)
display.printLine(apps[app_index][0], 3)

while True:
    buttons.update()

    if running:
        apps[app_index][1].update()
        if buttons.A_pressed:
            apps[app_index][1].exit()
            running = False
            display.clear()
            display.printLine("Select an app", 1)
            display.printLine(apps[app_index][0], 3)
    else:
        if buttons.Up_pressed:
            app_index = app_index + 1 if app_index + 1 < len(apps) else 0
            display.printLine(apps[app_index][0], 3)
        if buttons.A_pressed:
            pass
        if buttons.Down_pressed:
            app_index = app_index - 1 if app_index - 1 >= 0 else len(apps) - 1
            display.printLine(apps[app_index][0], 3)
        if buttons.B_pressed:
            display.printLine("Running...", 1)
            running = True

    time.sleep(0.01)

    #if useWifi:
    #    (ping, strength) = wifi.ping()
    #    display.printLine(f'p:{ping} s:{strength}', 3)