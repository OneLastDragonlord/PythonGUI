from tkinter import *
def About():
    print("This is a simple example of a menu")
    
top = Tk()
menu = Menu(top)
top.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="Home", menu=filemenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=top.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

mainloop()