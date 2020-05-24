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
        self.assembleButton = Button(self.frame,text = "Assemble", command = self.assemble, bg = "white")
        self.assembleButton.grid(row = 0, column = 0)
        self.runButton = Button(self.frame,text = "Run", state = "disabled", bg = "white", command = self.run)
        self.runButton.grid(row = 0, column = 1)
        self.stepButton = Button(self.frame,text = "Step", state = "disabled", bg = "white", command = self.step )
        self.stepButton.grid(row = 0, column = 2)
        self.resetButton = Button(self.frame,text = "Reset", state = "disabled", command = self.reset, bg = "white")
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
                self.reinitInterpreter(args)
                self.updateArgs(args)
                self.runButton["state"] = "normal"
                self.stepButton["state"] = "normal"
                self.resetButton["state"] = "normal"
                self.assembleButton["state"] = "disabled"
            else:
                self.report(errMsg)
        pass

    def reset(self):
        self.stop()
        self.runButton["state"] = "disabled"
        self.stepButton["state"] = "disabled"
        self.resetButton["state"] = "disabled"
        self.assembleButton["state"] = "normal"
        self.clearOutput()
        self.clearRam()

    def run(self):
        if self.runButton["text"] == "Run":
            self.exec(False)
            self.setInState(True)
            self.runButton["text"] = "Stop"
        else:
            self.runButton["text"] = "Run"
            self.stop()


    def step(self):
        self.exec(True)
        self.setInState(False)

    def stop(self):
        pass



    def assign_Functions(self,*args):
        self.getText = args[0]
        self.passed = args[1]
        self.updateArgs = args[2]
        self.report = args[3]
        self.reinitInterpreter = args[4]
        self.exec = args[5]
        self.setInState = args[6]
        self.clearOutput = args[7]
        self.clearRam = args[8]
        self.stop = args[9]
        pass
