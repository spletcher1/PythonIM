import HeadlessClasses
import time
import sys

if(sys.argv.__len__()!=2):
    print("Wrong number of arguments!")
    exit()

try:
    monitor_id = int(sys.argv[1])
except: 
    print("Bad UART ID argument!")
    exit()

theHardware=HeadlessClasses.MonitoringHardware(monitor_id)

counter=1

while True:
   uart = HeadlessClasses.MyUART(monitor_id)
   while True:
        s = "Counter: %d" % (counter)
        counter=counter+1
        uart.Write(s)
        print(s)
        time.sleep(2)

