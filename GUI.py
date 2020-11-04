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

        #menus
        menubar = tk.Menu(self)
        menubar.add_command(label="Scherm 1")
        menubar.add_command(label="Scherm 2")
        self.config(menu=menubar)

        #tabs
        tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text="Home")
        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text="Grafieken")
        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text="Instellingen")
        tabControl.pack(expand=1,fill="both")

        self.addingWidgets()
        #self.addingTabs()
    
    def addingWidgets(self):
        labelFrame1 = ttk.LabelFrame(self.tab1, text="first")
        labelFrame1.grid(column = 0, row = 0, padx = 8, pady = 10)
        label = ttk.Label(labelFrame1,text= "Enter your Name:")
        label.grid(column = 0, row = 0, sticky='W')

    def addingTabs(self):
        
        tabControl1 = ttk.Notebook(self.tab1)
        self.tab4 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab4, text="Scherm 1")
        self.tab5 = ttk.Frame(tabControl1)
        tabControl1.add(self.tab5, text="Scherm2")

if __name__ == '__main__':
    root = Root()
    root.mainloop()
