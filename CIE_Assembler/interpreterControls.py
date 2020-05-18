try:
    from Tkinter import *
except:
    from tkinter import *
import copy


class InterpreterControls:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(master)
        self.frame.grid(row = r, column = c, sticky = W)
        self.runButton = Button(self.frame,text = "Assemble", command = self.assemble)
        self.runButton.grid(row = 0, column = 0)
        self.runButton = Button(self.frame,text = "Run")
        self.runButton.grid(row = 0, column = 1)
        self.stepButton = Button(self.frame,text = "Step")
        self.stepButton.grid(row = 0, column = 2)
        self.resetButton = Button(self.frame,text = "Reset")
        self.resetButton.grid(row = 0, column = 3)
        self.getText = None


    def assemble(self):
        parsed = copy.deepcopy(self.getText())
        if parsed:
            ram,s = self.passed(parsed)
            ram = copy.deepcopy(ram)
            self.updateRam(ram)

        pass

    def assign_Functions(self,getText,passed ,updateRam):
        self.getText = getText
        self.passed = passed
        self.updateRam = updateRam

        pass
