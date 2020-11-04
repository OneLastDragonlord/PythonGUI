import tkinter as tk
def About():
    print("This is a simple example of a menu")
    
top = tk.Tk()
top.geometry("700x500")
menu = tk.Menu(top)
top.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label="Home", menu=filemenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=top.quit)

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

tk.mainloop()