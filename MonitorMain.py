import board
import digitalio
import busio
import time
import MonitorClasses
import _thread
import serial
import matplotlib.pyplot as plt



#uart= serial.Serial("/dev/ttyS0",baudrate=19200,timeout=3000)
i2c = busio.I2C(board.SCL, board.SDA)
tsl = MonitorClasses.TSL2561(i2c)
si =  MonitorClasses.SI7021(i2c)
theServer = MonitorClasses.MyServer()
theUART=MonitorClasses.MyUART(0x01)
_thread.start_new_thread(theServer.Start,())
_thread.start_new_thread(theUART.StartListening,())
##theData=MonitorClasses.DataHistory()



##print("Hello blinka")
##ledYellow=digitalio.DigitalInOut(board.D5)
##ledYellow.direction=digitalio.Direction.OUTPUT
##ledGreen=digitalio.DigitalInOut(board.D6)
##ledGreen.direction=digitalio.Direction.OUTPUT
##ledRed=digitalio.DigitalInOut(board.D13)
##ledRed.direction=digitalio.Direction.OUTPUT

##def ToggleLEDs():
##    if(ledYellow.value==True):
##        ledYellow.value=ledGreen.value=ledRed.value=False
##    else:
##        ledYellow.value=ledGreen.value=ledRed.value=True

while True:
    t=si.GetTemperature()
    l=tsl.GetLUX()
    h=si.GetHumidity()
##    ToggleLEDs()
    theServer.SetData(t,l,h)
    theUART.SetData(t,l,h)
##    theData.AddNewDataPoint(si.GetTemperature(),tsl.GetLUX(),si.GetHumidity())
##    theUART.Write('hi')
    time.sleep(1)
