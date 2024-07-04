import board
import digitalio
import busio
import time
import adafruit_tsl2561
import adafruit_tsl2591
import adafruit_si7021
import _thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver 
import serial
import PRelay

class TSL2591:
    def __init__(self,i2c):
        self.__Initialize(i2c)
    def __Initialize(self, i2c):
        self.theSensor = adafruit_tsl2591.TSL2591(i2c)
        self.theSensor.enabled=True
        # Enable the light sensor
        self.theSensor.enabled = True
        # Set default gain (LOW = 1; MED=25; HIGH=428; MAX=9876)
        self.theSensor.gain = adafruit_tsl2591.GAIN_MED 
        # Set integration time (intervals of 100ms)
        self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS
    def Set100msIntegrationTime(self):
        self.theSensor.integration_time=adafruit_tsl2591.INTEGRATIONTIME_100MS
    def Set200msIntegrationTime(self):
        self.theSensor.integration_time=adafruit_tsl2591.INTEGRATIONTIME_200MS
    def Set300msIntegrationTime(self):
        self.theSensor.integration_time=adafruit_tsl2591.INTEGRATIONTIME_300MS
    def Set400msIntegrationTime(self):
        self.theSensor.integration_time=adafruit_tsl2591.INTEGRATIONTIME_400MS
    def Set500msIntegrationTime(self):
        self.theSensor.integration_time=adafruit_tsl2591.INTEGRATIONTIME_500MS
    def Set600msIntegrationTime(self):
        self.theSensor.integration_time=adafruit_tsl2591.INTEGRATIONTIME_600MS
    def SetGainLow(self):
        self.theSensor.gain = adafruit_tsl2591.GAIN_LOW
    def SetGainMedium(self):
        self.theSensor.gain = adafruit_tsl2591.GAIN_MED
    def SetGainHigh(self):
        self.theSensor.gain = adafruit_tsl2591.GAIN_HIGH
    def SetGainMax(self):
        self.theSensor.gain = adafruit_tsl2591.GAIN_MAX
    def PrintAllInfo(self):
            visible = self.theSensor.visible
            infrared = self.theSensor.infrared
            fullspectrum = self.theSensor.full_spectrum
            lux = self.GetLUX()
            if(lux != -99) : 
                print("Gain = {}".format(self.theSensor.gain))
                print("Integration time = {}".format(self.theSensor.integration_time))
                print("Visible Light = {}".format(visible))
                print("Infrared = {}".format(infrared))
                print("Full spectrum = {}".format(fullspectrum))
                print("Lux = {}".format(lux))
            else :
                print("Adjusting sensitivity...")

    def IncreaseSensitivity(self):
        isMaxedOut=False
        if self.theSensor.gain == adafruit_tsl2591.GAIN_LOW :
            self.theSensor.gain = adafruit_tsl2591.GAIN_MED
        elif self.theSensor.gain == adafruit_tsl2591.GAIN_MED :
            self.theSensor.gain = adafruit_tsl2591.GAIN_HIGH
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_100MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_200MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_300MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_400MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS
        else :
            isMaxedOut = True
        return isMaxedOut

    def DecreaseSensitivity(self):
        isMaxedOut=False       
        if self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_500MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_400MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_300MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS
        elif self.theSensor.integration_time == adafruit_tsl2591.INTEGRATIONTIME_200MS :
            self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
        elif self.theSensor.gain == adafruit_tsl2591.GAIN_HIGH :
            self.theSensor.gain = adafruit_tsl2591.GAIN_MED
        elif self.theSensor.gain == adafruit_tsl2591.GAIN_MED :
            self.theSensor.gain = adafruit_tsl2591.GAIN_LOW
        else:
            isMaxedOut=True
        return isMaxedOut

    def GetLUX(self):
        try:
            lux = self.theSensor.lux
            if(lux<1.0):
                if (self.IncreaseSensitivity()):
                    return lux
                else :
                    return -99
            else:
                return lux
        # Circuitpython returns runtimeerror on overflow
        except RuntimeError: 
            if(self.DecreaseSensitivity()) :
                return 100000
            else :
                return -99
   
class MyRequestHandler(BaseHTTPRequestHandler):   
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        if self.server.isRelayOn:
            tmp = "<html><body>temp=%f;light=%f;humidity=%f;Relay=On</body></html>" % (self.server.temperature,self.server.light,self.server.humidity,)
        else:
            tmp = "<html><body>temp=%f;light=%f;humidity=%f;Relay=Off</body></html>" % (self.server.temperature,self.server.light,self.server.humidity,)
        #tmp = "%d;%f;%f;%f" % (self.server.temperature,self.server.light,self.server.humidity)
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>".encode())
        self.wfile.write(tmp.encode())
    def do_HEAD(self,s):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

class MyHTTPServer(HTTPServer):
    def __init__(self,server_address,requestHandlerClass):
        super().__init__(server_address,requestHandlerClass)
        self.temperature = 1
        self.light=2
        self.humidity=3
        self.isRelayOn = False
    def SetData(self,temp,light,humidity,isRelayOn):
        self.temperature = temp
        self.light=light
        self.humidity=humidity
        self.isRelayOn=isRelayOn

class MyServer():
    def __init__(self):
        self.server_address = ('', 50001)
        self.httpd = MyHTTPServer(self.server_address, MyRequestHandler)
    def Start(self):
        self.httpd.serve_forever()
    def SetData(self,temp,light,humidity,isRelayOn):
        self.httpd.SetData(temp,light,humidity,isRelayOn)
    
class SI7021:
    def __init__(self,i2c):
        self.__Initialize(i2c)
    def __Initialize(self,i2c):
        self.theSensor=adafruit_si7021.SI7021(i2c)
    def GetTemperature(self):
        return self.theSensor.temperature
    def GetHumidity(self):
        return self.theSensor.relative_humidity

class MonitoringHardware():
    def __init__(self,targetTemp):        
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.tsl = TSL2591(self.i2c)
        self.si =  SI7021(self.i2c)
        self.theRelay =  PRelay.PRelay(targetTemp)       
        self.theServer = MyServer()
        _thread.start_new_thread(self.theServer.Start,())
        
    def UpdateReadings(self):
        testing=False
        if(testing==False):
            self.temperature=self.si.GetTemperature()
            l=self.tsl.GetLUX()
            counter=0
            while (l == -99 and counter<10) :
                l=self.tsl.GetLUX()
                time.sleep(1)
                counter+=1
            self.light = l
            self.humidity=self.si.GetHumidity()
        else:
            self.light=100
            self.humidity=50
            self.temperature=25
        self.theRelay.UpdateRelays(self.temperature,self.light,self.humidity)
      
        self.theServer.SetData(self.temperature,self.light,self.humidity,self.theRelay.IsRelay0On())
        
        ## The following two lines are for testing only.
        ##tmp=self.theUART.GetDataString()
        ##self.theUART.Write(tmp)