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
        self.bars["File"] = Menu(self.toolbar)
        self.bars["Tools"] = Menu(self.toolbar)
        self.bars["Config"] = Menu(self.toolbar)
        self.bars["Help"] = Menu(self.toolbar)
        self.bars["About"] = Menu(self.toolbar)

        for each in self.bars:
            self.toolbar.add_cascade(label = each, menu = self.bars[each])
        self.master.config(menu = self.toolbar)

        self.bars["File"].add_command(label = "Save")
