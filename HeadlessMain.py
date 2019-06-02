import HeadlessClasses
import time
import sys

UPDATE_INTERVAL_SEC=60

if(sys.argv.__len__!=2):
    print("Wrong argument value!")
    exit()

monitor_id = sys.argv[1]
theHardware=HeadlessClasses.MonitoringHardware(monitor_id)

while True:
    theHardware.UpdateReadings()
    t=theHardware.temperature
    l=theHardware.light
    h=theHardware.humidity
    theHardware.theServer.SetData(t,l,h)
    theHardware.theUART.SetData(t,l,h)
    time.sleep(UPDATE_INTERVAL_SEC)

