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

wifi.radio.enabled = False
time.sleep(2)

while True:
    time.sleep(1)
    ipv4 = ipaddress.ip_address("192.168.10.1")
    try:
        if not wifi.radio.enabled:
            wifi.radio.enabled = True
            time.sleep(0.5)
        if wifi.radio.connected:
            ping = wifi.radio.ping(ipv4)
            strength = wifi.radio.ap_info.rssi
            free = espidf.heap_caps_get_free_size()
            print("Wifi ping: ", ping, "ms Strength: ", strength, "dB")
        else:
            try:
                print("Connecting to WiFi", os.getenv('CIRCUITPY_WIFI_SSID'), ", channel:", int(os.getenv('CIRCUITPY_WIFI_CHANNEL')))
                wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'), channel=int(os.getenv('CIRCUITPY_WIFI_CHANNEL')))
                print("Connected to WiFi")
                print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
                print("My IP address is", wifi.radio.ipv4_address)
                print("Channel is", wifi.radio.ap_info.channel)
            except Exception as e:
                print(f'caught {type(e)}: e')
                wifi.radio.enabled = False
                time.sleep(2)
            
    except Exception as e:
        print(f'caught {type(e)}: e')
