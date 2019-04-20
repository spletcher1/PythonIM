#import socketserver
import MonitorClasses
import board
import digitalio
import busio
import time

print("Hello blinka")

i2c = busio.I2C(board.SCL, board.SDA)
tsl = MonitorClasses.TSL2561(i2c)
