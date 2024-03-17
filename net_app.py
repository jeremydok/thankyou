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

    def entry(self):
        self.first = False

    def update(self, dt: float):
        if self.first:
            self.entry()

        if self.buttons.B_pressed:

            pass
        if self.buttons.up:
            self.wifi.connect()
        if self.buttons.down:
            (ping, strength) = self.wifi.ping()
            self.display.printLine(f"p:{ping} s:{strength}", 3)

    def exit(self):
        self.first = True
