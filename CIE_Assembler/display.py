try:
    from Tkinter import *
except:
    from tkinter import *

import copy

def denHex(x):
    # Converts a denary integer into a formatted hexadecimal string
    l =  hex(x)[2:].upper()
    if len(l) == 1:
        l = "0" + l
    return l


class Display:
    def __init__(self, master, r, c):
        self.master = master
        self.font = ("consolas", 12)
        self.frame = Frame(self.master)
        self.frame.grid(row = r, column = c)
        self.ramFrame = Frame(self.frame, borderwidth = 5, relief = "groove")
        self.ramFrame.grid(row = 1, column = 0)
        self.regFrame = Frame(self.frame,borderwidth = 5, relief = "groove")
        self.regFrame.grid(row = 0, column = 0, sticky = W)
        self.ram = [denHex(0) for i in range(256)] # a list of integers
        self.textArray = [] # a list of label objects
        self.convFunc = lambda x: x
        self.registers = {
            "IX":"1",
            "ACC":"1A",
            "PC":"0",
            "CMP":"0"
        }
        self.regArray = {}
        j = 0
        for reg in self.registers:
            self.regArray[reg+str("-label")] = Label(self.regFrame, text = reg, font = self.font, width = 5)
            self.regArray[reg+str("-label")].grid(row = 0,column = j)
            self.regArray[reg] = Label(self.regFrame, text = self.convFunc(self.registers[reg]), font = self.font)
            self.regArray[reg].grid(row = 1 , column = j)
            j+=1

        self.highlighted = {}

        #Loop to initialise the textArray
        j = 0
        for i in range(256):
            if i%16 == 0:
                j += 1
            self.textArray.append(Label(self.ramFrame, text = self.convFunc(self.ram[i]),font = self.font, width = 4 ))
            self.textArray[i].grid(row = j, column = i%16)


    def update(self):
        for reg in self.registers:
            self.regArray[reg]["text"] = self.convFunc(self.registers[reg])

        for i,data in enumerate(self.ram):
            self.textArray[i]["text"] = self.convFunc(data)


    def numSys(self, numSys):
        if numSys == "Hex":
            self.convFunc = lambda x: x
        elif numSys == "Dec":
            self.convFunc =  lambda x: "{:03d}".format(int(x,16))
        self.update()

        pass


    def add_hg(self,tag,ptrs):

        pass

    def remove_hg(self,tag):

        pass

    def updatePointer(self,ptrName):

        pass

    def updateRam(self,ram_):
        self.ram = copy.deepcopy(ram_)
        self.update()

        pass

if __name__ == "__main__":
    root = Tk()
    a = Assembler()
    a.init_RAM() #Creating RAM
    ram, s = a.passThrough([["JMP", "OTHERLABEL"],["LDD","174"],["LDD","174"],["LDD","174"],["LDD","174"],["OUT"],["LABELNAME", "END"],["OTHERLABEL", "LDM","252"]])
    r = Display(root,0,0)
    r.numSys("Hex")
    r.ram = ram
    r.update()




    root.mainloop()
