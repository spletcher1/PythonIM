import HeadlessClasses
import time
import sys
import PRelay

UPDATE_INTERVAL_SEC=10

if(sys.argv.__len__()!=2):
    print("Wrong number of arguments!")
    exit()
try:
    monitor_id = int(sys.argv[1])
except: 
    print("Bad UART ID argument!")
    exit()

theHardware=HeadlessClasses.MonitoringHardware(monitor_id)

while True:
    print("Updating readings")
    theHardware.UpdateReadings()   
    print("Done")
    time.sleep(UPDATE_INTERVAL_SEC)

