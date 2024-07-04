# Packages required for Incubator Control
# pip3 install adafruit-blinka
# pip3 install adafruit-circuitpython-tsl2591
# pip3 install adafruit-circuitpython-si7021
# pip3 install Phidget22

import HeadlessClasses
import time
import sys
import PRelay

UPDATE_INTERVAL_SEC=10
TARGET_TEMPERATURE = 32

theHardware=HeadlessClasses.MonitoringHardware(TARGET_TEMPERATURE)

while True:    
    theHardware.UpdateReadings()   
    t=theHardware.temperature
    l=theHardware.light
    h=theHardware.humidity   
    s= "Temp: %f   Humid: %f    Light:%f" % (t,h,l)
    print(s)
    time.sleep(UPDATE_INTERVAL_SEC)

 