# type : ignore
import os
import asyncio
import time
import array
import math

from board import *  # type: ignore
from busio import I2C  # type: ignore
import busio  # type: ignore
import espidf  # type: ignore

import digitalio  # type: ignore
import neopixel  # type: ignore

import audiocore  # type: ignore
import audiobusio  # type: ignore

from lis2hh12_accel import LIS2HH12
from wifi_code import thankyou_wifi
from buttons import Buttons
from display import Display

from app_base import AppBase
from level_app import LevelApp
from player import PlayerApp
from net_app import NetGetApp
from manny_app import manny

# Disable wifi so it has time to restart
use_wifi = os.getenv("USE_WIFI") == "True"

# Initialize I2C communication using IO6 and IO5 pins
i2c = I2C(IO6, IO5)

# Initialize the Display
display = Display(i2c)

# Clear the display
display.get().fill(0)
display.get().show()
display.printLine("J&M 4EVA", 1)

# Setup Accelerometer
device = LIS2HH12(i2c)
display.printLine("Accelerometer ready", 2)

# Setup NeoPixels
pixel_pin = IO4
num_pixels = 20
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()
display.printLine("Pixels ready", 2)

# Setup buttons
buttons = Buttons()
display.printLine("Buttons ready", 2)

# Setup audio
audio = audiobusio.I2SOut(IO44, IO7, IO8)
display.printLine("Audio ready", 2)

# blue_level = level(device, pixels)
apps = [
    ("Manny app", lambda: manny(device, display, buttons, pixels)),
    ("Level Red", lambda: LevelApp(device, pixels, (64, 0, 0))),
    ("Level Green", lambda: LevelApp(device, pixels, (0, 64, 0))),
    ("Level Blue", lambda: LevelApp(device, pixels, (0, 0, 64))),
    ("Play 2001", lambda: PlayerApp(audio, buttons, display)),
]
if use_wifi:
    wifi = thankyou_wifi()
    apps.append(("Network", lambda: NetGetApp(wifi, buttons, display)))

app_index = 0
running_app: Optional[AppBase] = None

display.clear()
display.printLine("Select an app", 1)
display.printLine(apps[app_index][0], 3)

last_update: float = 0

while True:
    buttons.update()

    if running_app is not None:
        dt = time.monotonic() - last_update
        running_app.update(dt)

        if buttons.A_pressed:
            running_app.exit()
            running_app = None

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
            running_app = apps[app_index][1]()
            last_update = time.monotonic()

    time.sleep(0.01)

    # if useWifi:
    #    (ping, strength) = wifi.ping()
    #    display.printLine(f'p:{ping} s:{strength}', 3)
