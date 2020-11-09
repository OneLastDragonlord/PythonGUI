#imports
import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter import Listbox
from time import strftime
import serial
# from PyQt5 import QtWidgets
# from pyqtgraph import PlotWidget, plot
# import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import time

#functions
class Root(Tk):
    def __init__(self):
        #window
        super(Root,self).__init__()
        self.title("Rolluik Legend")
        self.minsize(700,500)
        self.ser = serial.Serial('COM3', 9600)
        self.sendLichtgrens(3)
        time.sleep(2)
        #tabs
        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text="Scherm 1")
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Scherm 2")
        tabControl.pack(expand=1,fill="both")

        self.addingSubTabs(self.tab1)
        ##self.addingSubTabs(self.tab2)
    
    def addingSubTabs(self, tab):
        labelFrame1 = ttk.LabelFrame(tab)
        labelFrame1.grid(column = 0, row = 0, padx = 0, pady = 0)
        tabControl1 = ttk.Notebook(tab)
        self.tab3 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab3, text="Home")
        self.tab4 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab4, text="Grafieken")
        self.tab5 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab5, text="Instellingen")
        self.tab6 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab6)
        tabControl1.grid(column = 0, row = 0, sticky="W")
        self.addingHome(self.tab3, self.ser)
        self.addingGrafieken(self.tab4)
        self.addingInstellingen(self.tab5, self.ser)
        self.addNiks(self.tab6)

    # def grafieken (self):
    #     self.graphWidget = pg.PlotWidget()
    #     self.setCentralWidget(self.graphWidget)

    #     hour = [1,2,3,4,5,6,7,8,9,10]
    #     temperature = [30,32,34,32,33,31,29,32,35,45]

    #     # plot data: x, y values
    #     self.graphWidget.plot(hour, temperature)
    def readSerial(self,ser):
        b=''
        while ser.in_waiting >0:
            time.sleep(0.1)
            c = ser.read().decode('utf-8')
            if c != '\x00':
                b = b+c
        return b

    def sendDataHome(self, welke, ser):
        #status van auto verkrijgen en checken
        status =''
        self.randvariable = "get_status_auto*"
        ser.write(self.randvariable.encode('utf-8'))
        time.sleep(0.1)
        status = self.readSerial(ser)
        time.sleep(0.5)
        if (welke == "roll_in*" or welke == "roll_out*") and  status == '1OK':
            self.sendDataHome("set_manual*", ser)
            time.sleep(0.1)
        
        ser.write(welke.encode('utf-8'))
        if welke == "roll_in*" or welke == "roll_out*":
            time.sleep(5)
        else:
            time.sleep(0.5)
        b = self.readSerial(ser)
        if len(b) > 0:
            print(b)   
        print(welke)

    def getDataHome(self, welke, ser):
        time.sleep(0.5)
        ser.write(welke.encode('utf-8'))
        time.sleep(0.5)
        b = self.readSerial(ser)
        if len(b) > 0:
            print(b)   
        print(welke)
        return b
        
    def sendLichtgrens(self, getal):
        try:
            self.getalGrens = getal
        except:
            self.getalGrens = None
            
    def getAuto(self, ser):
        b = []
        self.randvariable = "get_status_auto*"
        ser.write(self.randvariable.encode('utf-8'))
        time.sleep(0.1)
        while ser.in_waiting >0:
            c = ser.read().decode('utf-8')
            if c != '\x00':
                b.append(c)
            time.sleep(0.1)
        print(b) 

    def addingHome(self,tab,ser):
        self.labelHome = tk.Label(tab, font = ('calibri', 50, 'bold'), 
            relief="solid",
            foreground = 'black')
        self.time()
        self.labelHome.pack(anchor="center")
        self.labelHome.place(y=100)
        self.labelHome.pack()
        self.addHomeButtons(tab,ser)
        

    

    def addHomeButtons(self, tab, ser):
        self.buttonAan = tk.Button(tab, text="In", command= lambda: self.sendDataHome("roll_in*", ser), width=15, height=3)
        self.buttonAan.pack()
        self.buttonAan.place(x=70, y=400)
        self.buttonUit = tk.Button(tab, text="Uit", command= lambda: self.sendDataHome("roll_out*", ser), width=15, height=3)
        self.buttonUit.pack()
        self.buttonUit.place(x=185, y=400)
        self.buttonAutAan = tk.Button(tab, text="Auto Aan", command= lambda: self.sendDataHome("set_auto*", ser), width=15, height=3)
        self.buttonAutAan.pack()
        self.buttonAutAan.place(x=330, y=400)
        self.buttonAutUit = tk.Button(tab, text="Auto Uit", command= lambda: self.sendDataHome("set_manual*", ser), width=15, height=3)
        self.buttonAutUit.pack()
        self.buttonAutUit.place(x=445, y=400)
        self.buttonStop = tk.Button(tab, text="Stop", command= lambda: self.sendDataHome("stop*", ser),width=15, height=3)
        self.buttonStop.pack()
        self.buttonStop.place(x=590, y=400)

    def addingGrafieken(self,tab):
        #self.grafieken()
        pass
        
        
    def addNiks(self, tab):
        self.labelFrame = ttk.LabelFrame(tab)
        self.labelFrame.grid(column = 0, row = 0, padx = 0, pady = 250)
        self.label = tk.Label(self.labelFrame, width=110)
        self.label.pack()
        

    def addingInstellingen(self,tab, ser):
        self.addGrafiekInstellingen(tab,ser)
        self.addCurrentInstellingen(tab,ser)

    def addGrafiekInstellingen(self,tab,ser):
        self.label2 = tk.Label(tab, text='Temperatuur grens (Celsius):')
        self.label2.place(x=20, y=20)
        self.setTemperatuur = tk.Entry(tab)
        self.setTemperatuur.place(x=25, y=55)
        self.label4 = tk.Label(tab, text='Lichtgrens:')
        self.label4.place(x=20, y=140)
        self.zeerLaag = tk.Button(tab, text="zeer laag", command= lambda: self.sendLichtgrens(1),width=11, height=2)
        self.zeerLaag.pack()
        self.zeerLaag.place(x=10, y=170)
        self.laag = tk.Button(tab, text="laag", command= lambda: self.sendLichtgrens(2),width=11, height=2)
        self.laag.pack()
        self.laag.place(x=97, y=170)
        self.gemiddeld = tk.Button(tab, text="gemiddeld", command= lambda: self.sendLichtgrens(3),width=11, height=2)
        self.gemiddeld.pack()
        self.gemiddeld.place(x=184, y=170)
        self.hoog = tk.Button(tab, text="hoog", command= lambda: self.sendLichtgrens(4),width=11, height=2)
        self.hoog.pack()
        self.hoog.place(x=271, y=170)
        self.zeerHoog = tk.Button(tab, text="zeer hoog", command= lambda: self.sendLichtgrens(5),width=11, height=2)
        self.zeerHoog.pack()
        self.zeerHoog.place(x=358, y=170)
        self.label3 = tk.Label(tab, text='Maximale uitrol (cm):')
        self.label3.place(x=20, y=265)
        self.maxUitrol = tk.Entry(tab)
        self.maxUitrol.place(x=25, y= 300)
        self.buttonMax = tk.Button(tab, text="Opslaan", command= lambda: self.stuurInstellingen(ser), width=15, height=3)
        self.buttonMax.pack()
        self.buttonMax.place(x=50, y=400)

    def addCurrentInstellingen(self, tab, ser):
        
        self.varTemperatuur = str(self.getCurrentInstellingen("get_limit_tempsensor*", ser)) + " ℃"
        self.varLichtgrens = self.getCurrentInstellingen("get_limit_lightsensor*", ser)
        self.varUitrol = str(self.getCurrentInstellingen("get_max*", ser)) + " cm"

        self.labelHuidig = tk.Label(tab, text='Intstellingen Scherm 1')
        self.labelHuidig.place(x=600, y=10)
        self.labelTempIngesteld = tk.Label(tab, text='Temperatuurgrens:')
        self.labelTempIngesteld.place(x=600, y=40)
        self.temperButton = tk.Button(tab, text=self.varTemperatuur, width=11, height=2)
        self.temperButton.pack()
        self.temperButton.place(x=600, y=60)
        self.labelLichtIngesteld = tk.Label(tab, text='Lichtgrens:')
        self.labelLichtIngesteld.place(x=600, y=80)
        self.lichtButton = tk.Button(tab, text=self.varLichtgrens, width=11, height=2)
        self.lichtButton.pack()
        self.lichtButton.place(x=600, y=100)
        self.labelUitrolIngesteld = tk.Label(tab, text= 'Uitrol:')
        self.labelUitrolIngesteld.place(x=600, y=120)
        self.uitrolButton = tk.Button(tab, text=self.varUitrol, width=11, height=2)
        self.uitrolButton.pack()
        self.uitrolButton.place(x=600, y=140)

    def getCurrentInstellingen(self,zin, ser):
        time.sleep(0.1)
        temp= self.getDataHome(zin, ser)
        time.sleep(0.1)
        if temp[-2:] == "OK":
            return temp[:-2]
        else:
            return "Niet goed"



    def stuurInstellingen(self, ser):
        try:
            self.dataTemperatuur = int(self.setTemperatuur.get())
            self.temperatuurSturen = "set_limit_tempsensor "+str(self.dataTemperatuur)+"*"
            ser.write(self.temperatuurSturen.encode('ascii'))
            print(self.temperatuurSturen)
        except:
            print("Geen geldige temperatuur")
        
        time.sleep(0.1) 

        self.getalGrens = str(self.getalGrens)
        self.lichtSturen = "set_limit_lightsensor "+self.getalGrens+"*"
        ser.write(self.lichtSturen.encode('ascii'))
        print(self.lichtSturen)
        
        time.sleep(0.1) 

        try:
            self.dataUitrol = int(self.maxUitrol.get())
            self.uitrolSturen = "set_max "+str(self.dataUitrol)+"*"
            ser.write(self.uitrolSturen.encode('ascii'))
            print(self.uitrolSturen)
        except:
            print("Geen geldige uitrol")
        
        



        # if isinstance(self.dataTemperatuur,int) or isinstance(self.dataTemperatuur,float):
        #     print(self.dataTemperatuur)
        # else:
        #     print("Geen geldige temperatuur")
            
        # if type(self.dataUitrol) == int or type(self.dataUitrol) == float:
        #     print(self.dataUitrol)
        # else:
        #     print("Geen geldige uitrol")
            
        #print(self.dataUitrol)
        #print(self.dataTemperatuur)
        #print(self.getalGrens)

    def time(self): 
        string = strftime('%H:%M:%S %p') 
        self.labelHome.config(text = string, borderwidth=10) 
        self.labelHome.place(x=215,y=100)
        self.labelHome.after(1000, self.time) 
    

if __name__ == '__main__':
    root = Root()
    root.mainloop()
