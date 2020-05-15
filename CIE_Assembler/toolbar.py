try:
    from Tkinter import *
except:
    from tkinter import *
from collections import OrderedDict

class ToolBar:
    def __init__(self, master):
        self.master = master
        self.toolbar = Menu(self.master)
        self.bars = OrderedDict()

        self.bars["File"] = Menu(self.toolbar, tearoff = False)
        self.bars["Edit"] = Menu(self.toolbar, tearoff = False)
        self.bars["Tools"] = Menu(self.toolbar, tearoff = False)
        self.bars["View"] = Menu(self.toolbar, tearoff = False)
        self.bars["About"] = Menu(self.toolbar, tearoff = False)


        self.numSys = Menu(self.bars["View"], tearoff = False)
        self.bars["View"].add_cascade(label = "NumberSystem", menu = self.numSys)
        self.numSys.add_command(label = "Decimal",command =  lambda: self.set_numSys("Dec"))
        self.numSys.add_command(label = "Hexadecimal", command = lambda: self.set_numSys("Hex"))




        for each in self.bars:
            self.toolbar.add_cascade(label = each, menu = self.bars[each])
        self.master.config(menu = self.toolbar)

        self.bars["File"].add_command(label = "Save")
        self.bars["File"].add_command(label = "Load")
        self.bars["Edit"].add_command(label = "Preferences")
        self.bars["Tools"].add_command(label = "Symbol Table")
        self.bars["Tools"].add_command(label = "Frequency")
        self.bars["About"].add_command(label = "Info")







    def save(self):

        pass

    def pop_load(self):
        pass

    def set_freq(self):

        pass

    def pop_symbol(self):

        pass



    def assign_numSys(self,func):
        self.set_numSys = func

        pass


    def pop_symbol(self):

        pass

    def pop_info(self):

        pass


if __name__ == "__main__":

    root = Tk()
    tb = ToolBar(root)


    root.mainloop()
