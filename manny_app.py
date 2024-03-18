# from app import app
from lis2hh12_accel import LIS2HH12
from display import Display
from buttons import Buttons
import neopixel
import math
import time
import random
from app_base import AppBase

class manny(AppBase):
    accelerometer = None
    display = None
    buttons = None
    pixels = None
    displaywidth = 128
    displayheight = 32
    shipwidth = 8
    shipheight = 2
    poscenter = 0
    posy = displayheight-shipheight
    bullets = []
    alienwidth = 6
    alienheight = 6
    numaliens = 10
    aliendistance = int((displaywidth - (numaliens*alienwidth)) / (numaliens+1))
    aliens = []
    chance = 0.05
    lives = 17
    kills = 0
    running = True

    def __init__(
        self, accelorometer: LIS2HH12, display: Display, buttons: Buttons, pixels: neopixel.NeoPixel
    ) -> None:
        self.accelerometer = accelorometer
        self.pixels = pixels
        self.display = display
        self.buttons = buttons
        self.display.clear()
        self.newalienline()
        self.checkLives()

    def update(self, dt: float):
        if not self.running:
            self.display.printLine("       GAME OVER  ", 2)
            self.display.printLine("       Score: {0}".format(self.kills), 3)
            return
        
        if self.buttons.B_pressed:
            self.bullets.append([int(self.poscenter),int(self.displayheight)])
        self.checkforhit()
        self.display.get().fill(0)
        self.drawship()
        self.drawbullet()
        self.drawaliens()
        self.display.get().show()
        
    def exit(self):
        self.pixels.fill((0, 0, 0))

    def drawrect(self, x, y):
        self.display.get().fill_rect(x,y,self.rectsize,self.rectsize,1)
        self.display.get().show()

    def drawship(self):
        (x, y, z) = self.accelerometer.acceleration
        maxx = 5
        minx = -5
        halfw = self.displaywidth / 2
        if x > maxx:
            x = maxx
        elif x < minx:
            x = minx

        self.poscenter = halfw - ((halfw/maxx)*x)
        posx = int(self.poscenter-self.shipwidth/2)
        self.display.get().fill_rect(posx,self.posy,self.shipwidth,self.shipheight,1)
        

    def drawbullet(self):
        if len(self.bullets) > 0:
            for bullet in self.bullets:
                self.display.get().fill_rect(bullet[0], bullet[1], 1,1,1)
                bullet[1]-=2
                if bullet[1] < 5:
                    self.bullets.remove(bullet)

    def drawaliens(self):
        for line in self.aliens:
            alienx = self.aliendistance
            alieny = line["y"]
            #for i in range(0,self.numaliens):
            for alien in line["aliens"]:
                if alien == 1:
                    self.display.get().fill_rect(alienx,alieny,self.alienwidth, self.alienheight, 1)
                    #print("X:{0:8.3f}, Y:{1:8.3f}".format(alienx, alieny))
                alienx += (self.alienwidth + self.aliendistance)
            line["y"] += 1
        
        if self.aliens[0]["y"] > self.displayheight:
            for a in self.aliens[0]["aliens"]:
                if a:
                    self.lives -= 1
            self.aliens.remove(self.aliens[0])
            self.checkLives()

        if self.aliens[-1]["y"] > self.aliendistance:
            self.newalienline()

    def newalienline(self):
        newline = {"y": 0, "aliens": []}
        newline["y"] = -self.alienheight
        for i in range(0,self.numaliens):
            newline["aliens"].append(random.random() < self.chance)
        self.chance += 0.01
        self.aliens.append(newline)

    def checkforhit(self):
        for bullet in self.bullets:
            for line in self.aliens:
                if bullet[1] > line["y"] and bullet[1] < line["y"] + self.alienheight:
                    alienindex = math.floor((bullet[0] - self.aliendistance) / (self.alienwidth + self.aliendistance))
                    if alienindex >= self.numaliens: # bullet might be further right than all aliens
                        break
                    if bullet[0] - self.aliendistance > alienindex * (self.alienwidth + self.aliendistance) - self.aliendistance:
                        if line["aliens"][alienindex] == 1:
                            line["aliens"][alienindex] = 0
                            self.bullets.remove(bullet)
                            self.kills += 1
                            self.checkHits()
                            break
    
    def checkHits(self):
        bonus = self.kills % 4
        print("k: {0} b: {1}".format(self.kills, bonus))
        for i in range(0, 3):
            if i >= bonus:
                self.pixels[19-i] = (0,0,0)
            else:
                self.pixels[19-i] = (0,0,64)
        if bonus == 0:
            self.lives = min(17, self.lives + 1)
            self.showLives()
        self.pixels.show()
    
    def checkLives(self):
        if self.lives <= 0:
            self.running = False
            self.pixels.fill((32,0,0))
            self.pixels.show()
            self.display.clear()
        else:
            self.showLives()

    def showLives(self):
        for i in range(0, 17):
            self.pixels[i] = (0,0,0)
        for i in range(0, self.lives):
            self.pixels[i] = (0,0,64)
        self.pixels.show()



