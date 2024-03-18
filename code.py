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
from pong_app import PongApp

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
imu = LIS2HH12(i2c)
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
    ("Manny app", lambda: manny(imu, display, buttons, pixels)),
    ("Level Red", lambda: LevelApp(imu, pixels, (64, 0, 0))),
    ("Level Green", lambda: LevelApp(imu, pixels, (0, 64, 0))),
    ("Level Blue", lambda: LevelApp(imu, pixels, (0, 0, 64))),
    ("Play 2001", lambda: PlayerApp(audio, buttons, display)),
    ("Pong", lambda: PongApp(imu, audio, buttons, pixels, display.display)),
]
if use_wifi:
    wifi = thankyou_wifi()
    apps.append(("Network", lambda: NetGetApp(wifi, buttons, display)))

app_index = 4
running_app: Optional[AppBase] = None

display.clear()
display.printLine("Select an app", 1)
display.printLine(apps[app_index][0], 3)

last_update: float = 0
soft_reset_start: Optional[float] = None

last_loop_time = 0
LOOP_PERIOD_SEC = 0.01

while True:
    # Sleep the necessary amount of time to keep period constant
    now = time.monotonic()
    dt = now - last_loop_time
    if dt < 0.01:
        time.sleep(LOOP_PERIOD_SEC - dt)
    last_loop_time = time.monotonic()

    buttons.update()

    if running_app is not None:
        # Reset check
        if buttons.A and buttons.B:
            if soft_reset_start is None:
                soft_reset_start = time.monotonic()
            else:
                dt = time.monotonic() - soft_reset_start
                if dt >= 5:
                    running_app.exit()
                    running_app = None

                    display.printLine("RESET", 1)
                    time.sleep(2)  # Give time for the user to let go of the buttons
                    continue
        else:
            soft_reset_start = None

        # Calculate app dt
        now = time.monotonic()
        dt = now - last_update
        last_update = now

        # Run app cycle
        running_app.update(dt)
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

    # if useWifi:
    #    (ping, strength) = wifi.ping()
    #    display.printLine(f'p:{ping} s:{strength}', 3)
