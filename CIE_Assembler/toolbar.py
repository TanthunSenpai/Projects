try:
    from Tkinter import *
except:
    from tkinter import *
from collections import OrderedDict
import time
import os

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

        self.bars["File"].add_command(label = "Save", command = lambda: self.save())
        self.bars["File"].add_command(label = "Load")
        self.bars["Edit"].add_command(label = "Preferences")
        self.bars["Tools"].add_command(label = "Symbol Table")
        self.bars["Tools"].add_command(label = "Frequency")
        self.bars["About"].add_command(label = "Info", command = self.pop_info)



    def get_text(self):
        text = ""
        return text



    def save(self):

        self.text =self.get_text()

        #change path
        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) +"\savedFile"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        #create file
        self.fileName =time.strftime("%d-%m-%y_%H-%M-%S",time.localtime())+".txt"
        self.f = open(self.fileName,"w")
        self.f.write(self.text)
        self.f.close()


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
        popup = Tk()
        popup.title("Info")
        font1 = ("Times", 14,"bold")
        font2 = ("Consolas",12,"italic")
        font3 = ("Times",12)
        lines = [
        ("CIE Assembly Virtual Machine",font1),
        ("This program is designed to run the assembly code of CIE A-levels specification and aid students in their studies of computing. Made by The CompSciGang of Oxford International College",font3),
        ("Project is led by:",font1),
        ("Nicholas Mulvey",font2),
        ("Dev team:",font1),
        ("Adi Bozzhanov - Head of coding",font2),
        ("Laveen Chandnani - Head of computing",font2),
        ("Tanthun Assawapitiyaporn - Head of engineering",font2),
        ("Martin Lee - Head of programming",font2),
        ("Version: 0.0",font1)
        ]
        labels = []

        for i,line in enumerate(lines):
            labels.append(Label(popup, text = line[0], font = line[1], wraplength = 550))
            labels[i].grid(row = i, column = 0)

        popup.mainloop()

        pass


if __name__ == "__main__":

    root = Tk()
    tb = ToolBar(root)
    #tb.save()


    root.mainloop()
