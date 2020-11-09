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
        self.ser1 = serial.Serial('COM4', 9600)
        self.ser2 = serial.Serial('COM3', 9600)
        
        self.sendLichtgrens(3)
        self.counter = 0
        time.sleep(2)
        #tabs
        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text="Scherm 1")
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Scherm 2")
        tabControl.pack(expand=1,fill="both")

        self.addingSubTabs(self.tab1, 1)
        self.addingSubTabs(self.tab2, 2)
    
    def addingSubTabs(self, tab, welkeser):
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
        if welkeser == 1:
            self.addingHome(self.tab3, self.ser1, welkeser)
            self.addingGrafieken(self.tab4)
            self.addingInstellingen(self.tab5, self.ser1, welkeser)
        if welkeser == 2:
            self.addingHome(self.tab3, self.ser2, welkeser)
            self.addingGrafieken(self.tab4)
            self.addingInstellingen(self.tab5, self.ser2, welkeser)
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

    def sendDataHome(self, welke, ser, welkeser):
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
            if c != '\x00' and c != '\x80':
                b.append(c)
            time.sleep(0.1)
        print(b) 

    def addingHome(self,tab,ser,welkeser):
        if welkeser == 1:
            self.labelHome = tk.Label(tab, font = ('calibri', 50, 'bold'), 
                relief="solid",
                foreground = 'black')
            self.time()
            self.labelHome.pack(anchor="center")
            self.labelHome.place(y=100)
            self.labelHome.pack()
        if welkeser == 2:
            self.labelHome2 = tk.Label(tab, font = ('calibri', 50, 'bold'), 
                relief="solid",
                foreground = 'black')
            self.time2()
            self.labelHome2.pack(anchor="center")
            self.labelHome2.place(y=100)
            self.labelHome2.pack()
        self.addHomeButtons(tab,ser, welkeser)
        

    

    def addHomeButtons(self, tab, ser, welkeser):
        if welkeser == 1:
            self.buttonAan = tk.Button(tab, text="In", command= lambda: self.sendDataHome("roll_in*", ser, welkeser), width=15, height=3)
            self.buttonAan.pack()
            self.buttonAan.place(x=70, y=400)
            self.buttonUit = tk.Button(tab, text="Uit", command= lambda: self.sendDataHome("roll_out*", ser, welkeser), width=15, height=3)
            self.buttonUit.pack()
            self.buttonUit.place(x=185, y=400)
            self.buttonAutAan = tk.Button(tab, text="Auto Aan", command= lambda: self.sendDataHome("set_auto*", ser, welkeser), width=15, height=3)
            self.buttonAutAan.pack()
            self.buttonAutAan.place(x=330, y=400)
            self.buttonAutUit = tk.Button(tab, text="Auto Uit", command= lambda: self.sendDataHome("set_manual*", ser, welkeser), width=15, height=3)
            self.buttonAutUit.pack()
            self.buttonAutUit.place(x=445, y=400)
            self.buttonStop = tk.Button(tab, text="Stop", command= lambda: self.sendDataHome("stop*", ser, welkeser),width=15, height=3)
            self.buttonStop.pack()
            self.buttonStop.place(x=590, y=400)
        if welkeser == 2:
            self.buttonAan = tk.Button(tab, text="In", command= lambda: self.sendDataHome("roll_in*", ser, welkeser), width=15, height=3)
            self.buttonAan.pack()
            self.buttonAan.place(x=70, y=400)
            self.buttonUit = tk.Button(tab, text="Uit", command= lambda: self.sendDataHome("roll_out*", ser, welkeser), width=15, height=3)
            self.buttonUit.pack()
            self.buttonUit.place(x=185, y=400)
            self.buttonAutAan = tk.Button(tab, text="Auto Aan", command= lambda: self.sendDataHome("set_auto*", ser, welkeser), width=15, height=3)
            self.buttonAutAan.pack()
            self.buttonAutAan.place(x=330, y=400)
            self.buttonAutUit = tk.Button(tab, text="Auto Uit", command= lambda: self.sendDataHome("set_manual*", ser, welkeser), width=15, height=3)
            self.buttonAutUit.pack()
            self.buttonAutUit.place(x=445, y=400)
            self.buttonStop = tk.Button(tab, text="Stop", command= lambda: self.sendDataHome("stop*", ser, welkeser),width=15, height=3)
            self.buttonStop.pack()
            self.buttonStop.place(x=590, y=400)
            

    def addingGrafieken(self, ser):
        # self.dfTemp = DataFrame(data,columns=['Time','Temperature'])
        # figureTemp = plt.Figure(dpi=100)
        # axTemp = figureTemp.add_subplot(111)
        # lineTemp = FigureCanvasTkAgg(figureTemp, self.tab4)
        # lineTemp.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        # self.dfTemp = self.dfTemp[['Time','Temperature']].groupby('Time').sum()
        # self.dfTemp.plot(kind='line', legend=True, ax=axTemp, color='r',marker='o', fontsize=10)
        # axTemp.set_title('Time Vs. Temperature')

        # self.refreshButton = tk.Button(tab, text='refresh',command=lambda: self.updateGrafieken(tab))
        # self.refreshButton.pack()

        # self.dataLight = {'Time': ['15:31','15:32', '15:33','15:34','15:35', '15:36','15:37','15:38', '15:39'],
        #  'Light': [250, 300, 350, 400,450, 400, 350, 300 ,250]
        # }
        # self.dfLight = DataFrame(self.dataLight,columns=['Time','Light'])
        # self.figureLight = plt.Figure(dpi=100)
        # axLight = self.figureLight.add_subplot(111)
        # lineLight = FigureCanvasTkAgg(self.figureLight, self.tab4)
        # lineLight.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        # self.dfLight = self.dfLight[['Time','Light']].groupby('Time').sum()
        # self.dfLight.plot(kind='line', legend=True, ax=axLight, color='r',marker='o', fontsize=10)
        # axLight.set_title('Time Vs. Light')
        pass
 
    # def updateGrafieken(self,tab):
    #     self.figureLight.clear()
        
        
    def addNiks(self, tab):
        self.labelFrame = ttk.LabelFrame(tab)
        self.labelFrame.grid(column = 0, row = 0, padx = 0, pady = 250)
        self.label = tk.Label(self.labelFrame, width=110)
        self.label.pack()
        

    def addingInstellingen(self,tab, ser, welkeser):
        self.addGrafiekInstellingen(tab,ser, welkeser)
        self.addCurrentInstellingen(tab,ser)

    def addGrafiekInstellingen(self,tab,ser, welkeser):
        self.label2 = tk.Label(tab, text='Temperatuur grens (Celsius):')
        self.label2.place(x=20, y=20)
        if welkeser == 1:
            self.setTemperatuur = tk.Entry(tab)
            self.setTemperatuur.place(x=25, y=55)
        if welkeser == 2:
            self.setTemperatuur2 = tk.Entry(tab)
            self.setTemperatuur2.place(x=25, y=55)
        self.label4 = tk.Label(tab, text='Lichtgrens:')
        self.label4.place(x=20, y=140)
        self.zeerLaag = tk.Button(tab, text="zeer laag", command= lambda: self.sendLichtgrens(200),width=11, height=2)
        self.zeerLaag.pack()
        self.zeerLaag.place(x=10, y=170)
        self.laag = tk.Button(tab, text="laag", command= lambda: self.sendLichtgrens(350),width=11, height=2)
        self.laag.pack()
        self.laag.place(x=97, y=170)
        self.gemiddeld = tk.Button(tab, text="gemiddeld", command= lambda: self.sendLichtgrens(500),width=11, height=2)
        self.gemiddeld.pack()
        self.gemiddeld.place(x=184, y=170)
        self.hoog = tk.Button(tab, text="hoog", command= lambda: self.sendLichtgrens(650),width=11, height=2)
        self.hoog.pack()
        self.hoog.place(x=271, y=170)
        self.zeerHoog = tk.Button(tab, text="zeer hoog", command= lambda: self.sendLichtgrens(800),width=11, height=2)
        self.zeerHoog.pack()
        self.zeerHoog.place(x=358, y=170)
        self.label3 = tk.Label(tab, text='Maximale uitrol (cm):')
        self.label3.place(x=20, y=265)
        if welkeser == 1:
            self.maxUitrol = tk.Entry(tab)
            self.maxUitrol.place(x=25, y= 300)
        if welkeser == 2:
            self.maxUitrol2 = tk.Entry(tab)
            self.maxUitrol2.place(x=25, y= 300)
        self.buttonMax = tk.Button(tab, text="Opslaan", command= lambda: self.stuurInstellingen(tab, ser, welkeser), width=15, height=3)
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
        self.temperButton.place(x=600, y=70)
        self.labelLichtIngesteld = tk.Label(tab, text='Lichtgrens:')
        self.labelLichtIngesteld.place(x=600, y=125)
        self.lichtButton = tk.Button(tab, text=self.varLichtgrens, width=11, height=2)
        self.lichtButton.pack()
        self.lichtButton.place(x=600, y=155)
        self.labelUitrolIngesteld = tk.Label(tab, text= 'Uitrol:')
        self.labelUitrolIngesteld.place(x=600, y=210)
        self.uitrolButton = tk.Button(tab, text=self.varUitrol, width=11, height=2)
        self.uitrolButton.pack()
        self.uitrolButton.place(x=600, y=240)

    def getCurrentInstellingen(self,zin, ser):
        time.sleep(0.1)
        temp= self.getDataHome(zin, ser)
        time.sleep(0.1)
        if temp[-2:] == "OK":
            return temp[:-2]
        else:
            return "Niet goed"



    def stuurInstellingen(self, tab, ser, welkeser):
        if welkeser == 1:
            self.dataTemperatuur = int(self.setTemperatuur.get())
        if welkeser == 2:
            self.dataTemperatuur = int(self.setTemperatuur2.get())
        self.temperatuurSturen = "set_limit_tempsensor "+str(self.dataTemperatuur)+"*"
        ser.write(self.temperatuurSturen.encode('ascii'))
        time.sleep(0.1)
        temp = self.readSerial(ser)
        if temp[-2:] == "OK":
            print(self.temperatuurSturen)
        else:
            error = self.handshake(temp, self.temperatuurSturen, ser)
            if error == "hersteld":
                print("error temperatuur instellen is " + error)
            elif error == "niet hersteld":
                print("error temperatuur instellen is " + error)
            elif error == "onbekende error":
                print("onbekende error bij temperatuur instellen")
            else:
                print("er is een grote fout bij het temperatuur instellen..")

        time.sleep(0.5) 

        self.getalGrens = str(self.getalGrens)
        self.lichtSturen = "set_limit_lightsensor "+self.getalGrens+"*"
        ser.write(self.lichtSturen.encode('ascii'))
        time.sleep(0.1)
        temp = self.readSerial(ser)
        if temp[-2:] == "OK":
            print(self.lichtSturen)
        else:
            error = self.handshake(temp, self.lichtSturen, ser)
            if error == "hersteld":
                print("error lichtsturen is " + error)
            elif error == "niet hersteld":
                print("error lichtsturen is " + error)
            elif error == "onbekende error":
                print("onbekende error bij instellen lichtsturen")
            else:
                print("er is een grote fout met het instellen van de lichtgrens..")

        
        time.sleep(0.5) 

        
        if welkeser == 1:
            self.dataUitrol = int(self.maxUitrol.get())
        if welkeser == 2:
            self.dataUitrol = int(self.maxUitrol2.get())
        self.uitrolSturen = "set_max "+str(self.dataUitrol)+"*"
        ser.write(self.uitrolSturen.encode('ascii'))
        time.sleep(0.1)
        temp = self.readSerial(ser)
        if temp[-2:] == "OK":
            print(self.uitrolSturen)
        else:
            error = self.handshake(temp, self.uitrolSturen, ser)
            if error == "hersteld":
                print("error uitrol " + error)
            elif error == "niet hersteld":
                print("error uitrol " + error)
            elif error == "onbekende error":
                print("onbekende error bij het instellen van de uitrol")
            else:
                print("er is een grote fout met de uitrolwaarde..")

        time.sleep(0.1)
        self.addCurrentInstellingen(tab, ser)
        
    def handshake(self,received, send, ser):
        if received == "ERR_1" or received == "ERR_2":
            ser.write("handshake*".encode('utf-8'))
            time.sleep(0.2)
            temp = self.readSerial(ser)
            print("Deze temp is leeg of ONLINE" + temp)
            if self.counter < 4:
                if temp == "":
                    self.counter = self.counter + 1
                    self.handshake(received, send, ser)
                elif temp == "ONLINE":
                    ser.write(send.encode('utf-8'))
                    returnvalue = "hersteld"
                    self.counter = 0
                    return returnvalue
                else:
                    returnvalue = "onbekende error"
                    self.counter = 0
                    return returnvalue
            else:
                returnvalue = "niet hersteld"
                self.counter = 0
                return returnvalue



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

    def time2(self)
        string = strftime('%H:%M:%S %p') 
        self.labelHome2.config(text = string, borderwidth=10) 
        self.labelHome2.place(x=215,y=100)
        self.labelHome2.after(1000, self.time2) 
        
    def isint(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
    

if __name__ == '__main__':
    root = Root()
    root.mainloop()
