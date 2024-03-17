import ssl
import wifi
import socketpool
import adafruit_requests

from wifi_code import thankyou_wifi
from buttons import Buttons
from display import Display
from app_base import AppBase

class NetGetApp(AppBase):
    def __init__(self, wifi: thankyou_wifi, buttons: Buttons, display: Display) -> None:
        self.wifi = wifi
        self.buttons = buttons
        self.display = display
        self.first = True
        self.connect()

    def connect(self):
        self.display.printLine(f"Connecting...", 2)
        self.wifi.connect()
        if self.wifi.connected():
            self.display.printLine(f"Setup pools...", 2)
            self.pool = socketpool.SocketPool(wifi.radio)
            self.requests = adafruit_requests.Session(self.pool, ssl.create_default_context())
            self.display.printLine(f"Connected", 2)
        else:
            self.display.printLine(f"Not Connected. Press Up to connect.", 2)

    def update(self, dt: float):
        if self.buttons.B_pressed:
            self.display.printLine(f"Downloading...", 2)
            response = self.requests.get("https://dokter.family/mannyjeremy/thankyou/test.txt")
            print(response.text)
            self.display.printLine(f"Response:", 2)
            self.display.printLine(f"{response.text}", 3)
            
        if self.buttons.up:
            self.connect()
        if self.buttons.down:
            (ping, strength) = self.wifi.ping()
            self.display.printLine(f"p:{ping} s:{strength}", 3)

    def exit(self):
        self.first = True
