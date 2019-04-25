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
import matplotlib.pyplot as plt
import numpy as np
import tkinter
import serial
import matplotlib
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg

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
  


class DataPlot():
    def __init__(self,name,canvas):
        self.title=name
        self.temp=[0,0]
        self.humidity=[1,1]
        self.light=[2,2]
        font = {'size' : 12}  
        matplotlib.rc('font', **font)
        self.theFig = Figure(figsize=(8, 4.35), dpi=100)
        self.axis=self.theFig.add_subplot(111)
        self.plotCanvas=canvas
        self.plotType="temp"
        self.UpdatePlot()
    def ClearPlot(self):
        self.axis.clear()
        self.theplot=self.draw_figure(self.plotCanvas,self.theFig)
    def UpdatePlot(self):
        self.ClearPlot()
        self.axis.set_xlabel("Date")
        if self.plotType=="temp":
            self.axis.plot(self.temp,'r-s')
            self.axis.set_title("Temperature")
            self.axis.set_ylabel("Celsius")
        elif self.plotType=="humidity":
            self.axis.plot(self.humidity,'b-o')
            self.axis.set_title("Humidity")
            self.axis.set_ylabel("Relative Humidity (%)")
        elif self.plotType=="light":
            self.axis.plot(self.light,'k-^')
            self.axis.set_title("Light Level")
            self.axis.set_ylabel("LUX")
        self.theplot=self.draw_figure(self.plotCanvas,self.theFig)
    def AddNewDataPoint(self,ttemp,tlight,thumidity):
        if len(self.temp) < 200:
            self.temp.append(ttemp)
            self.light.append(tlight)
            self.humidity.append(thumidity)
            self.UpdatePlot()
        else:
            self.temp=np.roll(self.temp,-1)
            self.temp[199]=ttemp
            self.light=np.roll(self.light,-1)
            self.light[199]=tlight
            self.humidity=np.roll(self.humidity,-1)
            self.humidity[199]=thumidity
            self.UpdatePlot()
    def draw_figure(self,canvas, figure, loc=(0, 0)):
        """ Draw a matplotlib figure onto a Tk canvas
        loc: location of top-left corner of figure on canvas in pixels.
        Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
        """
        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

        # Position: convert from top-left anchor to center anchor
        canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
        #canvas.create_image(loc[0], loc[1], image=photo)
        # Unfortunately, there's no accessor for the pointer to the native renderer
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

        # Return a handle which contains a reference to the photo object
        # which must be kept live or else the picture disappears
        return photo

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
                
class TSL2591:
    def __init__(self,i2c):
        self.__Initialize(i2c)
    def __Initialize(self, i2c):
        self.theSensor = adafruit_tsl2591.TSL2591(i2c)
        self.theSensor.enabled=True
        # Enable the light sensor
        self.theSensor.enabled = True
        # Set gain 0=16x, 1=1x
        self.theSensor.gain = adafruit_tsl2591.GAIN_MED 
        # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
        self.theSensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
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
        visible = self.theSensor.visible
        infrared = self.theSensor.infrared
        fullspectrum = self.theSensor.fullspectrum
        # Get raw (luminosity) readings using tuple unpacking
        #broadband, infrared = tsl.luminosity
        # Get computed lux value (tsl.lux can return None or a float)
        lux = self.theSensor.lux
        print("Gain = {}".format(self.theSensor.gain))
        print("Integration time = {}".format(self.theSensor.integration_time))
        print("Visible Light = {}".format(visible))
        print("Infrared = {}".format(infrared))
        print("Full spectrum = {}".format(fullspectrum))
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

class MonitoringHardware():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.tsl = TSL2561(self.i2c)
        self.si =  SI7021(self.i2c)
        self.theServer = MyServer()
        self.theUART=MyUART(0x01)
        _thread.start_new_thread(self.theServer.Start,())
        _thread.start_new_thread(self.theUART.StartListening,())
    def UpdateReadings(self):
        self.temperature=self.si.GetTemperature()
        self.light=self.tsl.GetLUX()
        self.humidity=self.si.GetHumidity()
