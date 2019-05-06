import matplotlib.pyplot as plt
import numpy as np
import tkinter
import matplotlib
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import HeadlessClasses



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