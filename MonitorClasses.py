import board
import digitalio
import busio
import time
import adafruit_tsl2561
import adafruit_si7021
import _thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver 
import matplotlib.pyplot as plt
import numpy as np
import tkinter
import serial

class DataHistory:
    def __init__(self):
        self.temp=np.zeros(200)
        self.humidity=np.zeros(200)
        self.light=np.zeros(200)
        self.fig, self.ax = plt.subplots(3,1,figsize=(10,5))  
        self.ax[0].grid()
        self.ax[1].grid()
        self.ax[2].grid()
        self.ax[0].set_ylabel("Temperature")
        self.ax[1].set_title("Humidity")
        self.ax[2].set_title("Light")      
        mng=plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        self.isPlotRunning = False
        self.fig.show()
        self.fig.canvas.draw()
        plt.ion()        
    def AddNewDataPoint(self,ttemp,tlight,thumidity):
        self.temp=np.roll(self.temp,-1)
        self.temp[199]=ttemp
        self.light=np.roll(self.light,-1)
        self.light[199]=tlight
        self.humidity=np.roll(self.humidity,-1)
        self.humidity[199]=thumidity
        self.UpdatePlot()
    def UpdatePlot(self):
        self.ax[1].clear()
        self.ax[2].clear()
        self.ax[0].clear()
        self.ax[0].set_ylabel("Temperature")
        self.ax[1].set_ylabel("Humidity")
        self.ax[2].set_ylabel("Light")       
        self.ax[0].grid()
        self.ax[1].grid()
        self.ax[2].grid()
        self.ax[0].plot(self.temp,'r-s')
        self.ax[1].plot(self.humidity,'b-o')
        self.ax[2].plot(self.light,'k-^')
        self.fig.canvas.draw()
  
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
    def SetData(self,temp,light,humidity):
        self.temperature = temp
        self.light=light
        self.humidity=humidity
    def StartListening(self):
        while True:
            ser_bytes=self.thePort.read(3)
            if(ser_bytes[0]==self.startByte and ser_bytes[2]==self.endByte and ser_bytes[1]==self.ID):
                tmp = "<html><body>temp=%f;light=%f,humidity=%f</body></html>" % (self.temperature,self.light,self.humidity,)
                print(tmp)
            else:
                print('not for me')
                
                


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
        tmp = "<html><body>temp=%f;light=%f,humidity=%f</body></html>" % (self.server.temperature,self.server.light,self.server.humidity,)
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

