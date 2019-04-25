import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import matplotlib

import numpy as np

class DataPlot():
    def __init__(self,name,canvas):
        self.title=name
        self.temp=[0,0]
        self.humidity=[1,1]
        self.light=[2,2]
        font = {'size' : 20}  
        matplotlib.rc('font', **font)
        self.theFig = Figure(figsize=(20, 15), dpi=100)
        self.axis=self.theFig.add_subplot(111)
        self.plotCanvas=canvas
        self.plotType="temp"
        self.UpdatePlot()
    def ClearPlot(self):
        self.axis.clear()
        self.theplot=self.draw_figure(self.plotCanvas,self.theFig)
    def UpdatePlot(self):
        self.ClearPlot()
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


class App():
    def __init__(self, master):
        self.master=master
        master.title("Incubator Data")
        self.temp_button=tk.Button(master,text="Temperature",command=self.ShowTemperature,height=3, width=20)
        self.humid_button=tk.Button(master,text="Humidity",command=self.ShowHumidity,height=3, width=20)
        self.light_button=tk.Button(master,text="Light",command=self.ShowLight,height=3, width=20)
        self.temp_button.grid()
        self.humid_button.grid(column=1,row=0)
        self.light_button.grid(column=2,row=0)
        self.plotCanvas = tk.Canvas(master, width=2000, height=1500)
        self.plotCanvas.grid(columnspan=3)
        self.thePlot=DataPlot("test",self.plotCanvas)
        self.UpdateData()
    def getPlot(self):
        return self.thePlot
    def write_slogan(self):
        print ("Tkinter is easy to use!")
        self.thePlot.ClearPlot()
    def ShowTemperature(self):
        self.thePlot.plotType="temp"
        self.thePlot.UpdatePlot()
    def ShowHumidity(self):
        self.thePlot.plotType="humidity"
        self.thePlot.UpdatePlot()
    def ShowLight(self):
        self.thePlot.plotType="light"
        self.thePlot.UpdatePlot()
    def UpdateData(self):
        self.thePlot.AddNewDataPoint(10,15,20)
        self.thePlot.UpdatePlot()
        self.master.after(1000, self.UpdateData)


root=tk.Tk()
myGui=App(root)
root.mainloop()

