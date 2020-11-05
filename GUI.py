#imports
import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter import Listbox
from time import strftime
import serial

#functions
class Root(Tk):
    
    def __init__(self):
        #window
        super(Root,self).__init__()
        self.title("Rolluik Legend")
        self.minsize(700,500)
        self.ser = serial.Serial('COM3', 9600)
        #tabs
        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text="Scherm 1")
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Scherm 2")
        tabControl.pack(expand=1,fill="both")

        self.addingSubTabs(self.tab1)
        #self.addingSubTabs(self.tab2)
    
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
        tabControl1.grid(column = 0, row = 0, sticky="W")
        self.addingHome(self.tab3, self.ser)
        self.addingGrafieken(self.tab4)
        self.addingInstellingen(self.tab5)
        #self.addHomeknoppen(self.tab3)
    
    def sendDataHome(self, welke, ser):
        if welke == "In":
            ser.write("roll_in")
            #print("Hij gaat in")
        if welke == "Uit":
            print("Hij gaat uit")
        if welke == "AutAan":
            print("Hij is auto aan")
        if welke == "AutUit":
            print("Hij is auto uit")
        if welke == "Stop":
            print("Stop")
        
    def addingHome(self,tab,ser):
        self.labelHome = ttk.Label(tab, font = ('calibri', 40, 'bold'), 
            background = 'purple', 
            foreground = 'white') 
        self.time()
        #elelele
        self.labelHome.pack(anchor="center")
        self.labelHome.pack()
        self.buttonAan = tk.Button(tab, text="In", command= lambda: self.sendDataHome("In", ser), width=15, height=3)
        self.buttonAan.pack()
        self.buttonAan.place(x=70, y=400)
        self.buttonUit = tk.Button(tab, text="Uit", command= lambda: self.sendDataHome("Uit", ser), width=15, height=3)
        self.buttonUit.pack()
        self.buttonUit.place(x=185, y=400)
        self.buttonAutAan = tk.Button(tab, text="Aan", command= lambda: self.sendDataHome("AutAan", ser), width=15, height=3)
        self.buttonAutAan.pack()
        self.buttonAutAan.place(x=330, y=400)
        self.buttonAutUit = tk.Button(tab, text="Uit", command= lambda: self.sendDataHome("AutUit", ser), width=15, height=3)
        self.buttonAutUit.pack()
        self.buttonAutUit.place(x=445, y=400)
        self.buttonStop = tk.Button(tab, text="Stop", command= lambda: self.sendDataHome("Stop", ser),width=15, height=3)
        self.buttonStop.pack()
        self.buttonStop.place(x=590, y=400)
        
    # def addHomeKnoppen(self,tab):
    #     self.buttonAan = tk.Button(self.tab, text ="Aan", width=15, height=2)
    #     self.buttonAan.pack()
    #     self.buttonAan.place(x=100, y=300)

    def addingGrafieken(self,tab):
        #labelFrame = ttk.LabelFrame(tab)
        #labelFrame.grid(column = 0, row = 0, padx = 0, ipady = 250)
        self.label = tk.Label(tab,text = "Home", width=30)
        self.label.grid(row = 50, column = 100)
        #label.pack(expand=True)
        

    def addingInstellingen(self,tab):
        self.labelFrame = ttk.LabelFrame(tab, text="Huidige Instellingen")
        self.labelFrame.grid(column = 0, row = 0, padx = 0, pady = 250)
        self.label = ttk.Label(self.labelFrame,text = "Home", width=120)
        self.label.grid( sticky="E")

    def time(self): 
        string = strftime('%H:%M:%S %p') 
        self.labelHome.config(text = string) 
        self.labelHome.after(1000, self.time) 

    

if __name__ == '__main__':
    root = Root()
    root.mainloop()
