from tkinter import *

master = Tk()

w = Canvas(master, width=1280, height=720)
w.pack()

w.create_line(0, 0, 1280, 720)

w.create_line(0, 0, 700, 720)
w.pack()
master.mainloop()
