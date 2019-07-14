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

class MyUART:
    def __init__(self, ID):
        self.thePort=serial.Serial('/dev/ttyS0',19200)
        self.ID = ID
        self.temperature = 1
        self.light=2
        self.humidity=3
        self.startByte=0x40 #'@'
        self.endByte=0x23   #'#'
    def Write(self,s):
        self.thePort.write(s.encode())
    def GetDataString(self):
        tmp = "%d;%f;%f;%f" % (self.ID,self.temperature,self.light,self.humidity)
        return tmp
    def SetData(self,temp,light,humidity):
        self.temperature = temp
        self.light=light
        self.humidity=humidity
    def StartListening(self):
        while True:
            ser_byte=self.thePort.read()
            if(ser_byte[0]==self.startByte):
                ser_bytes=self.thePort.read(2) 
                if(ser_bytes[1]==self.endByte and ser_bytes[0]==self.ID):
                    tmp = self.GetDataString()
                    print(tmp)
                    self.Write(tmp)
                else:
                    print('ID=%d is not for me or endBye (=%d) incorrect.' % (ser_bytes[0],  ser_bytes[1]))
                    #print(ser_bytes)
            else:
                print('Bad Packet %d', ser_byte[0])
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

class TSL2561:
    def __init__(self,i2c):
        self.__Initialize(i2c)
    def __Initialize(self, i2c):
        self.theSensor = adafruit_tsl2561.TSL2561(i2c)
        self.theSensor.enabled=True
        # Enable the light sensor
        self.theSensor.enabled = True
        # Set gain 0=16x, 1=1x
        self.theSensor.gain = 0 
        # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
        self.theSensor.integration_time = 1
    def SetShortIntegrationTime(self):
        self.theSensor.integration_time=0
    def SetMediumIntegrationTime(self):
        self.theSensor.integration_time=1
    def SetLongIntegrationTime(self):
        self.theSensor.integration_time=2
    def PrintAllInfo(self):
        #Get raw (luminosity) readings individually
        broadband = self.theSensor.broadband
        infrared = self.theSensor.infrared
        # Get raw (luminosity) readings using tuple unpacking
        #broadband, infrared = tsl.luminosity
        # Get computed lux value (tsl.lux can return None or a float)
        try:
            lux = self.theSensor.lux
            print("Chip ID = {}".format(self.theSensor.chip_id))
            print("Enabled = {}".format(self.theSensor.enabled))
            print("Gain = {}".format(self.theSensor.gain))
            print("Integration time = {}".format(self.theSensor.integration_time))
            print("Broadband = {}".format(broadband))
            print("Infrared = {}".format(infrared))
            if lux is not None:
                print("Lux = {}".format(lux))
            else:
                print("Lux value is None. Possible sensor underrange or overrange.")   
        except RuntimeError:
            print("Runtime Error!")
    def SetHighGain(self):
        self.theSensor.gain=0
    def SetLowGain(self):
        self.theSensor.gain=1
    def GetLUX(self):
        lux = self.theSensor.lux
        if(lux=="None"):
            if(self.theSensor.gain==0):
                self.SetLowGain()
            elif(self.theSensor.gane==1):
                self.SetHighGain()                
            time.sleep(0.5)
            lux = self.theSensor.lux
        return lux
    
class MyRequestHandler(BaseHTTPRequestHandler):   
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        tmp = "<html><body>temp=%f;light=%f;humidity=%f</body></html>" % (self.server.temperature,self.server.light,self.server.humidity,)
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
    def SetData(self,temp,light,humidity):
        self.temperature = temp
        self.light=light
        self.humidity=humidity

class MyServer():
    def __init__(self):
        self.server_address = ('', 50001)
        self.httpd = MyHTTPServer(self.server_address, MyRequestHandler)
    def Start(self):
        self.httpd.serve_forever()
    def SetData(self,temp,light,humidity):
        self.httpd.SetData(temp,light,humidity)
    
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
    def __init__(self,uartID):
        self.uartID = uartID
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.tsl = TSL2591(self.i2c)
        self.si =  SI7021(self.i2c)
        if(self.uartID==0):
            self.theServer = MyServer()
            _thread.start_new_thread(self.theServer.Start,())
        else:
            self.theUART=MyUART(uartID)
            _thread.start_new_thread(self.theUART.StartListening,())        
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
        
        if(self.uartID==0):
            self.theServer.SetData(self.temperature,self.light,self.humidity)
        else:
            self.theUART.SetData(self.temperature,self.light,self.humidity)
        ## The following two lines are for testing only.
        ##tmp=self.theUART.GetDataString()
        ##self.theUART.Write(tmp)
    



if __name__=="__main__" :
    #i2c = busio.I2C(board.SCL, board.SDA)
    #tsl = TSL2591(i2c)
    uart = MyUART(1)
    while True:
        uart.Write("Hi there::")
        print("Hi there::")
        #tsl.PrintAllInfo()
        time.sleep(2)
    