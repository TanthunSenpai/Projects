try:
    from Tkinter import *
except:
    from tkinter import *


class EditorButtons:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(master)
        self.frame.grid(row = r, column = c, sticky = W)
        self.runButton = Button(self.frame,text = "Run")
        self.runButton.grid(row = 0, column = 0)
        self.stepButton = Button(self.frame,text = "Step")
        self.stepButton.grid(row = 0, column = 1)
        self.resetButton = Button(self.frame,text = "Reset")
        self.resetButton.grid(row = 0, column = 2)
