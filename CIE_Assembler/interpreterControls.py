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
        self.assembleButton = Button(self.frame,text = "Assemble", command = self.assemble)
        self.assembleButton.grid(row = 0, column = 0)
        self.runButton = Button(self.frame,text = "Run", state = "disabled")
        self.runButton.grid(row = 0, column = 1)
        self.stepButton = Button(self.frame,text = "Step", state = "disabled")
        self.stepButton.grid(row = 0, column = 2)
        self.resetButton = Button(self.frame,text = "Reset", state = "disabled")
        self.resetButton.grid(row = 0, column = 3)
        self.getText = None

    def update_sym(self,sym):

        pass


    def assemble(self):
        parsed = copy.deepcopy(self.getText())
        if parsed:
            isValid, args, sym, errMsg = self.passed(parsed)
            self.update_sym(sym)
            if isValid:
                args = copy.deepcopy(args)
                self.updateArgs(args)
                self.runButton["state"] = "normal"
                self.stepButton["state"] = "normal"
                self.resetButton["state"] = "normal"
                self.assembleButton["state"] = "disabled"
            else:
                self.report(errMsg)
        pass

    def assign_Functions(self,getText,passed ,updateArgs,report):
        self.getText = getText
        self.passed = passed
        self.updateArgs = updateArgs
        self.report = report
        pass
