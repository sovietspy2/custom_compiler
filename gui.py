from tkinter import *

master = Tk()

w = Canvas(master, width=1280, height=720)
w.pack()

w.create_line(0, 0, 1280, 720)

widget = Label(w, text='Spam', fg='white', bg='black')
w.create_window(1000, 100, window=widget)
master.mainloop()

