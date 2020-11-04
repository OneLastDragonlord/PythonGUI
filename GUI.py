#imports
import tkinter as tk
from tkinter import ttk
from tkinter import Tk

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
        labelFrame1 = ttk.LabelFrame(tab, text="first")
        labelFrame1.grid(column = 0, row = 0, padx = 0, pady = 0)
        tabControl1 = ttk.Notebook(tab)
        self.tab3 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab3, text="Home")
        self.tab4 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab4, text="Grafieken")
        self.tab5 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab5, text="Instellingen")
        tabControl1.grid(column = 0, row = 0)
        

if __name__ == '__main__':
    root = Root()
    root.mainloop()
