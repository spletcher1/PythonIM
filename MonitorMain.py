import MonitorClasses
import tkinter as tk

class App():
    def __init__(self, master):
        self.master=master
        master.title("Incubator Data")
        self.state = False
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)
        self.master.attributes('-zoomed', True) 
        self.toggle_fullscreen()
        self.temp_button=tk.Button(master,text="Temperature",command=self.ShowTemperature,height=2, width=15)
        self.humid_button=tk.Button(master,text="Humidity",command=self.ShowHumidity,height=2, width=15)
        self.light_button=tk.Button(master,text="Light",command=self.ShowLight,height=2, width=15)
        self.fullscreen_button=tk.Button(master,text="FullScreen",command=self.toggle_fullscreen,height=2, width=15)
        self.temp_button.grid()
        self.humid_button.grid(column=1,row=0)
        self.light_button.grid(column=2,row=0)
        self.fullscreen_button.grid(column=3,row=0)
        self.plotCanvas = tk.Canvas(master, width=800, height=480)
        self.plotCanvas.grid(columnspan=4,row=1)
        self.thePlot=MonitorClasses.DataPlot("test",self.plotCanvas)
        self.theHardware=MonitorClasses.MonitoringHardware()
        self.UpdateData()
    
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.state)
        return "break"
    def end_fullscreen(self, event=None):
        self.state = False
        self.master.attributes("-fullscreen", False)
        return "break"
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
        self.theHardware.UpdateReadings()
        t=self.theHardware.temperature
        l=self.theHardware.light
        h=self.theHardware.humidity
        self.thePlot.AddNewDataPoint(t,l,h)
        self.theHardware.theServer.SetData(t,l,h)
        self.theHardware.theUART.SetData(t,l,h)
        self.thePlot.UpdatePlot()
        self.master.after(1000, self.UpdateData)


root=tk.Tk()
myGui=App(root)
root.mainloop()

#uart= serial.Serial("/dev/ttyS0",baudrate=19200,timeout=3000)
#i2c = busio.I2C(board.SCL, board.SDA)
#tsl = MonitorClasses.TSL2561(i2c)
#si =  MonitorClasses.SI7021(i2c)
#theServer = MonitorClasses.MyServer()
#theUART=MonitorClasses.MyUART(0x01)
#_thread.start_new_thread(theServer.Start,())
#_thread.start_new_thread(theUART.StartListening,())
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


