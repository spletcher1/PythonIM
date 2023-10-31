from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *
import time
import datetime


class PRelay:
    def onAttach(self,tmp):
        print("Attach!")

    def onDetach(self,tmp):
        print("Detach!")

    def __init__(self):
        self.relay0 = DigitalOutput()
        self.relay0.setChannel(0)
        self.relay1 = DigitalOutput()
        self.relay1.setChannel(1)
        self.relay2 = DigitalOutput()
        self.relay2.setChannel(2)
        self.relay3 = DigitalOutput()
        self.relay3.setChannel(3)

        #self.relay0.setOnAttachHandler(self.onAttach)
        #self.relay0.setOnDetachHandler(self.onDetach)
        #self.relay1.setOnAttachHandler(self.onAttach)   
        #self.relay1.setOnDetachHandler(self.onDetach)
        #self.relay2.setOnAttachHandler(self.onAttach)
        #self.relay2.setOnDetachHandler(self.onDetach)
        #self.relay3.setOnAttachHandler(self.onAttach)
        #self.relay3.setOnDetachHandler(self.onDetach)

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
        print("Here")
        if(temp<34):
            self.relay0.setDutyCycle(1)
            self.relay1.setDutyCycle(1)
            self.relay2.setDutyCycle(1)
            self.relay3.setDutyCycle(1)
            print("Heat on")
        elif(temp>38):
            self.relay0.setDutyCycle(0)
            self.relay1.setDutyCycle(0)
            self.relay2.setDutyCycle(0)
            self.relay3.setDutyCycle(0)
            print("Heat off")        

    def CheckRelay0(self):
        timeOn=8
        timeOff=20
        isLightOn=False
        tmp=datetime.datetime.now()
        if(tmp.hour>=timeOn and tmp.hour<timeOff):
            isLightOn=True                        
        if (isLightOn):
            self.relay0.setDutyCycle(1)
        else:
            self.relay0.setDutyCycle(0)

    def CheckRelay1(self):
        timeOn=8
        timeOff=20
        isLightOn=False
        tmp=datetime.datetime.now()
        if(tmp.hour>=timeOn and tmp.hour<timeOff):
            isLightOn=True                        
        if (isLightOn):
            self.relay1.setDutyCycle(1)
        else:
            self.relay1.setDutyCycle(0)

    def CheckRelay2(self): #Bottom Heat Lights
        timeOn=8
        timeOff=20
        isLightOn=False
        tmp=datetime.datetime.now()
        if(tmp.hour>=timeOn and tmp.hour<timeOff):
            isLightOn=True                        
        if (isLightOn):
            self.relay2.setDutyCycle(1)
        else:
            self.relay2.setDutyCycle(0)

    def CheckRelay3(self): #Bottom lights
        self.relay3.setDutyCycle(0)


    def TempWorker(self):
        counter=0
        while True:
            #if counter % 5 == 0:
            #    print(counter)
            self.CheckRelay0()
            self.CheckRelay1()
            self.CheckRelay2()
            self.CheckRelay3()
            time.sleep(10)
            #counter+=1




def main():
    tmp = PRelay()
    tmp.TempWorker()

def main2():
    while True:
        try:
            tmp=datetime.datetime.now()
            print(tmp)
            time.sleep(1)
        except:
            print("Error!")
            time.sleep(1)
