import ipaddress
import wifi
import socketpool
import os
import time

class thankyou_wifi:
    lastping = 0
    ping_interval = 2
    def __init__(self):
        wifi.radio.enabled = False
        self.lastping = 0
        print("new wifi instance")
            
    def reset(self, offtime=2):
        #printLine(f'Resetting.', 3)
        wifi.radio.enabled = False
        time.sleep(2)
    
    def connected(self):
        return wifi.radio.connected

    def radio(self):
        return wifi.radio

    def connect(self):
        if wifi.radio.enabled:
            try:
                #printLine(f'Connecting...', 3)
                print("Connecting to WiFi", os.getenv('CIRCUITPY_WIFI_SSID'), ", channel:", int(os.getenv('CIRCUITPY_WIFI_CHANNEL')))
                wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'), channel=int(os.getenv('CIRCUITPY_WIFI_CHANNEL')))
                print("Connected to WiFi")
                print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
                print("My IP address is", wifi.radio.ipv4_address)
                print("Channel is", wifi.radio.ap_info.channel)
            except Exception as e:
                print(f'caught {type(e)}: e')
                self.reset()
        else:
            wifi.radio.enabled = True
            time.sleep(0.5)

    def ping(self, ping_adr=ipaddress.ip_address('8.8.8.8')):
        if wifi.radio.connected:
            try:
                if time.monotonic() - self.lastping > self.ping_interval:
                    ping = wifi.radio.ping(ping_adr)
                    if ping:
                        ping *= 1000
                    strength = wifi.radio.ap_info.rssi
                    self.lastping = time.monotonic()
                    #printLine(f'p:{ping} s:{strength}', 3)
                    print("ping: ", ping)
                    return (ping, strength)
            except Exception as e:
                print(f'caught e:{e} type:{type(e)}')
        else:
            self.connect()
        return (None, None)