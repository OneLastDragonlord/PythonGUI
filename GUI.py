#imports
import tkinter as tk
from tkinter import ttk
from tkinter import Tk

#functions
class Root(Tk):
    def __init__(self):
    #window
        super(Root,self).__init__()
        self = tk.Tk()
        self.geometry("700x500")

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
         #start GUI
        

    def addingWidgets(self):
        labelFrame = ttk.LabelFrame(self.tab1, text="first")
        labelFrame.grid(column = 0, row = 0, padx = 8, pady = 10)

if __name__ == '__main__':
    root = Root()
    root.mainloop()
