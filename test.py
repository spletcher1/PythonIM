#import socketserver
import MonitorClasses
import board
import digitalio
import busio
import time

print("Hello blinka")

i2c = busio.I2C(board.SCL, board.SDA)
tsl = MonitorClasses.TSL2591(i2c)
#uart = MonitorClasses.MyUART(1)
while True:
    #uart.Write("Hi there::")
    #print("Hi there::")
    tsl.PrintAllInfo()
    time.sleep(2)
    