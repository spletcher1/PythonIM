from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import time
import datetime


class PRelay:
    def onAttach(self,tmp):
        print("Attach!")

    def onDetach(self,tmp):
        print("Detach!")

    def __init__(self,targetTemp):
        self.relay0 = DigitalOutput()
        self.relay0.setChannel(0)
        self.relay1 = DigitalOutput()
        self.relay1.setChannel(1)
        self.relay2 = DigitalOutput()
        self.relay2.setChannel(2)
        self.relay3 = DigitalOutput()
        self.relay3.setChannel(3)

        self.targetTemperature = targetTemp     

        self.relay0.openWaitForAttachment(1000)
        self.relay0.setDutyCycle(0)
        self.relay1.openWaitForAttachment(1000)
        self.relay1.setDutyCycle(0)
        self.relay2.openWaitForAttachment(1000)
        self.relay2.setDutyCycle(0)
        self.relay3.openWaitForAttachment(1000)
        self.relay3.setDutyCycle(0)
        print("Relays Initialized")

    def IsRelay0On(self):
        return self.relay0.getState()

    def UpdateRelays(self,temp,light,humidity):        
        if(temp<self.targetTemperature-2):
            self.relay0.setDutyCycle(1)
            self.relay1.setDutyCycle(1)
            self.relay2.setDutyCycle(1)
            self.relay3.setDutyCycle(1)
            print("Heat on")
        elif(temp>self.targetTemperature+2):
            self.relay0.setDutyCycle(0)
            self.relay1.setDutyCycle(0)
            self.relay2.setDutyCycle(0)
            self.relay3.setDutyCycle(0)
            print("Heat off")        