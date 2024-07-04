import HeadlessClasses
import time
import sys


theHardware=HeadlessClasses.MonitoringHardware()

while True:
    theHardware.UpdateReadings()
    t=theHardware.temperature
    l=theHardware.light
    h=theHardware.humidity   
    s= "Temp: %f   Humid: %f    Light:%f." % (t,h,l)
    print(s)
    time.sleep(3)

