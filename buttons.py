import digitalio
from board import *

class Buttons:
    def __init__(self) -> None:
        self.ASwitch = digitalio.DigitalInOut(IO9)
        self.ASwitch.direction = digitalio.Direction.INPUT
        self.ASwitch.pull = digitalio.Pull.UP
        self.APressed = False
        self.ALatch = False

        self.BSwitch = digitalio.DigitalInOut(IO2)
        self.BSwitch.direction = digitalio.Direction.INPUT
        self.BSwitch.pull = digitalio.Pull.UP
        self.BPressed = False
        self.BLatch = False

        self.upSwitch = digitalio.DigitalInOut(IO1)
        self.upSwitch.direction = digitalio.Direction.INPUT
        self.upSwitch.pull = digitalio.Pull.UP
        self.UPressed = False
        self.ULatch = False

        self.downSwitch = digitalio.DigitalInOut(IO3)
        self.downSwitch.direction = digitalio.Direction.INPUT
        self.downSwitch.pull = digitalio.Pull.UP
        self.DPressed = False
        self.DLatch = False

    @property
    def A(self):
        return not self.ASwitch.value

    @property
    def A_pressed(self):
        if self.APressed:
            self.APressed = False
            return True
        else:
            return False

    @property
    def B(self):
        return not self.BSwitch.value

    @property
    def B_pressed(self):
        if self.BPressed:
            self.BPressed = False
            return True
        else:
            return False
    
    @property
    def up(self):
        return not self.upSwitch.value

    @property
    def Up_pressed(self):
        if self.UPressed:
            self.UPressed = False
            return True
        else:
            return False

    @property
    def down(self):
        return not self.downSwitch.value

    @property
    def Down_pressed(self):
        if self.DPressed:
            self.DPressed = False
            return True
        else:
            return False
    
    def update(self):
        if not self.ALatch and not self.ASwitch.value:
            self.ALatch = True
        if self.ALatch and self.ASwitch.value:
            self.ALatch = False
            self.APressed = True  
    
        if not self.BLatch and not self.BSwitch.value:
            self.BLatch = True
        if self.BLatch and self.BSwitch.value:
            self.BLatch = False
            self.BPressed = True  

        if not self.ULatch and not self.upSwitch.value:
            self.ULatch = True
        if self.ULatch and self.upSwitch.value:
            self.ULatch = False
            self.UPressed = True  

        if not self.DLatch and not self.downSwitch.value:
            self.DLatch = True
        if self.DLatch and self.downSwitch.value:
            self.DLatch = False
            self.DPressed = True  