import board
import busio
import struct
import time

from lis2hh12_accel import LIS2HH12

i2c = busio.I2C(board.IO6,board.IO5)

while not i2c.try_lock():
    pass
print("Found i2c devices:", [hex(x) for x in i2c.scan()])
i2c.unlock()
    
device = LIS2HH12(i2c)
print("LIS2HH12 WHO_AM_I:", hex(device.whoami))

while True:
    print(device.acceleration)
    time.sleep(0.5)