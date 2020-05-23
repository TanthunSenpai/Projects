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
    #This is a display widget

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
        self.lineNums = [] # a list containing line number labels in display

        self.registers = {
            "PC": "00",
            "IX":"00",
            "ACC":"00",
            "ZMP":"00",
            "HLT": "00",
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
                self.lineNums.append(Label(self.ramFrame,text = denHex(j)[1]+"~", font = self.font, fg = "blue"))
                self.lineNums[j].grid(row = j, column = 0)
                j+= 1
            self.textArray.append(Label(self.ramFrame, text = self.convFunc(self.ram[i]),font = self.font, width = 4 ))
            self.textArray[i].grid(row = j-1, column = i%16+1)




    def update(self):
        for reg in self.registers:
            self.regArray[reg]["text"] = self.convFunc(int(self.registers[reg]))

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

    def updateArgs(self,args):
        arggs = copy.deepcopy(args)
        self.registers["ACC"] = arggs["ACC"]
        self.registers["IX"] = arggs["IX"]
        self.registers["PC"] = arggs["PC"]
        self.registers["ZMP"] = arggs["ZMP"]
        self.registers["HLT"] = arggs["halt"]
        self.ram = arggs["RAM"]
        self.update()

        pass

if __name__ == "__main__":
    root = Tk()
    d = Display(root,0,0)
    dic = {
        "PC" :14,
        "IX" :3,
        "ACC" : 13,
        "ZMP" : 0,
        "HLT" : 0,
        "RAM" : ["01" for _ in range(256)]

    }
    d.updateArgs(dic)




    root.mainloop()
