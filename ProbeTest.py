import HeadlessClasses
import time

UART_MONITOR_ID = 0x01
UART_MONITOR_NAME = "Test incubator"

theHardware=HeadlessClasses.MonitoringHardware(UART_MONITOR_ID)

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

