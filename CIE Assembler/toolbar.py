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

        for each in self.bars:
            self.toolbar.add_cascade(label = each, menu = self.bars[each])
        self.master.config(menu = self.toolbar)

        self.bars["File"].add_command(label = "Save")
        self.bars["File"].add_command(label = "Load")
        self.bars["Edit"].add_command(label = "Preferences")
        self.bars["Tools"].add_command(label = "Symbol Table")
        self.bars["Tools"].add_command(label = "Frequency")
        self.bars["View"].add_command(label = "Show")
        self.bars["View"].add_command(label = "Number System")
        self.bars["About"].add_command(label = "Credits")
        self.bars["About"].add_command(label = "Version")
        self.bars["About"].add_command(label = "Documentation")
