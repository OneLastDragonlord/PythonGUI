#imports
import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter import Listbox
from time import strftime

#functions
class Root(Tk):
    def __init__(self):
        #window
        super(Root,self).__init__()
        self.title("Rolluik Legend")
        self.minsize(700,500)

        #tabs
        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text="Scherm 1")
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Scherm 2")
        tabControl.pack(expand=1,fill="both")

        self.addingSubTabs(self.tab1)
        self.addingSubTabs(self.tab2)
    
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
        self.addingHome(self.tab3)
        self.addingGrafieken(self.tab4)
        self.addingInstellingen(self.tab5)
        
    def addingHome(self,tab):
        Root.labelHome = ttk.Label(tab, font = ('calibri', 40, 'bold'), 
            background = 'purple', 
            foreground = 'white') 
        Root.time()
        Root.labelHome.pack(anchor="center")
        Root.labelHome.pack()
        

    def addingGrafieken(self,tab):
        labelFrame = ttk.LabelFrame(tab)
        labelFrame.grid(column = 0, row = 0, padx = 0, pady = 0)
        label = ttk.Label(labelFrame,text = "Home", width=120)
        label.grid(column = 0, row = 0, sticky="W")

    def addingInstellingen(self,tab):
        labelFrame = ttk.LabelFrame(tab, text="Huidige Instellingen")
        labelFrame.grid(column = 0, row = 0, padx = 0, pady = 0)
        label = ttk.Label(labelFrame,text = "Home", width=120)
        label.grid( sticky="E")

    def time(): 
        string = strftime('%H:%M:%S %p') 
        Root.labelHome.config(text = string) 
        Root.labelHome.after(1000, Root.time) 

if __name__ == '__main__':
    root = Root()
    root.mainloop()
