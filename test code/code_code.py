from board import *
from busio import I2C
import busio
import adafruit_ssd1306
import neopixel
import espidf

import time
import array
import math
import audiocore
import audiobusio

import os
import ipaddress
import wifi
import socketpool

import digitalio
import asyncio

from lis2hh12_accel import LIS2HH12

def printLine(text, line):
    y = 0
    y = (line * 10) - 10
    display.fill_rect(0,y,128,10,0)
    display.text(text, 0, y, 1)
    display.show()

#Disable wifi so it has time to restart
wifi.radio.enabled = False
useWifi = True

# Initialize I2C communication using IO6 and IO5 pins
i2c = I2C(IO6,IO5)

# Create a display object with 128x32 resolution and an I2C address of 0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3C)

# Clear the display
display.fill(0)
display.show()
printLine('J&M 4EVA', 1)

# Setup Accelerometer
device = LIS2HH12(i2c)

pixel_pin = IO4
num_pixels = 20
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=True)
pixels.fill((0,0,0))
pixels.show()

printLine('Pixels ready', 2)
time.sleep(0.5)

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

audio = audiobusio.I2SOut(IO44, IO7, IO8)
sample_rate = 100000
tone_volume = .05  # Increase or decrease this to adjust the volume of the tone.
frequency = 440  # Set this to the Hz of the tone you want to generate.
length = sample_rate // frequency  # One freqency period
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))

wave_file = open("2001.wav", "rb")
wave = audiocore.WaveFile(wave_file)
sine_wave_sample = audiocore.RawSample(sine_wave, sample_rate=sample_rate)

printLine('Audio ready', 2)
time.sleep(0.5)

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

lastping = 0
while True:
    count = 0
    if not upSwitch.value:
        pixels.fill((128,128,255))
        printLine('On', 2)
    if not rightSwitch.value:
        printLine('Play', 2)
        audio.play(wave)
    if not downSwitch.value:
        printLine('Off', 2)
        pixels.fill((0,0,0))
    if not leftSwitch.value:
        printLine('Stop', 2)
        audio.stop()
    (x,y,z) = device.acceleration
    XYAngle = (math.atan2(x,y)/math.pi*180) + 180
    printLine(f'a:{XYAngle}', 1)

    if useWifi:
        ping_adr = ipaddress.ip_address('192.168.10.1')
        ping_interval = 2
        try:
            if not wifi.radio.enabled:
                wifi.radio.enabled = True
                printLine('Radio Enable', 3)
                time.sleep(0.5)
            if wifi.radio.connected:
                if time.monotonic() - lastping > ping_interval:
                    ping = wifi.radio.ping(ping_adr) * 1000
                    strength = wifi.radio.ap_info.rssi
                    lastping = time.monotonic()
                    printLine(f'p:{ping} s:{strength}', 3)
                    print("ping: ", ping)
            else:
                try:
                    printLine(f'Connecting...', 3)
                    print("Connecting to WiFi", os.getenv('CIRCUITPY_WIFI_SSID'), ", channel:", int(os.getenv('CIRCUITPY_WIFI_CHANNEL')))
                    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'), channel=int(os.getenv('CIRCUITPY_WIFI_CHANNEL')))
                    print("Connected to WiFi")
                    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
                    print("My IP address is", wifi.radio.ipv4_address)
                    print("Channel is", wifi.radio.ap_info.channel)
                except Exception as e:
                    print(f'caught {type(e)}: e')
                    printLine(f'Resetting.', 3)
                    wifi.radio.enabled = False
                    time.sleep(2)
        except Exception as e:
            print(f'caught {type(e)}: e')

