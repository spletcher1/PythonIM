import HeadlessClasses
import time
import sys

if(sys.argv.__len__!=2):
    print("Wrong number of arguments!")
    exit()

try:
    monitor_id = int(sys.argv[1])
except: 
    print("Bad UART ID argument!")
    exit()

theHardware=HeadlessClasses.MonitoringHardware(monitor_id)

while True:
    theHardware.UpdateReadings()
    t=theHardware.temperature
    l=theHardware.light
    h=theHardware.humidity
    theHardware.theServer.SetData(t,l,h)
    theHardware.theUART.SetData(t,l,h)
    s= "Temp: %f   Humid: %f    Light:%f." % (t,h,l)
    print(s)
    time.sleep(3)

