try:
    from Tkinter import *
except:
    from tkinter import *

def hexStr(num):
    return str(hex(num))[2:].upper()



class RamDisplay:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.grid(row = r, column = c)
        self.ramFrame = Frame(self.frame, borderwidth = 5, relief = "groove")
        self.ramFrame.grid(row = 0, column = 0)
        self.ram = [0 for i in range(256)] # a list of integers
        self.textArray = [] # a list of label objects
        self.registers = {}
        self.highlighted = {}

        #Loop to initialise the textArray
        j = 0
        for i in range(256):
            if i%16 == 0:
                j += 1
            self.textArray.append(Label(self.ramFrame, text = hexStr(i))) # the format thingy is converting denary i into hex
            self.textArray[i].grid(row = j, column = i%16)


    def update(self):
        for i,data in enumerate(self.ram):
            self.textArray[i].configure(text = hexStr(data))

        self.master.update()


    def add_hg(self,tag,ptrs):

        pass

    def remove_hg(self,tag):

        pass

    def updatePointer(self,ptrName):

        pass

    def updateRam(self,ram_):

        pass

if __name__ == "__main__":
    root = Tk()
    r = RamDisplay(root,0,0)
    r.ram[0] = 15
    r.update()



    root.mainloop()
