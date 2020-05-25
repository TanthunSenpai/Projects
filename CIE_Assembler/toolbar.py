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
        self.verStr = "None"

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
        self.bars["File"].add_command(label = "Load", command = lambda: self.pop_load())
        self.bars["Edit"].add_command(label = "Preferences")
        self.bars["Tools"].add_command(label = "Symbol Table", command = lambda: self.pop_symbol())
        self.freq = Menu(self.bars["Tools"], tearoff = False)
        self.bars["Tools"].add_cascade(label = "Frequency", menu=  self.freq)
        self.freq.add_command(label = "1 HZ",command =  lambda: self.set_freq(1))
        self.freq.add_command(label = "2 HZ",command =  lambda: self.set_freq(2))
        self.freq.add_command(label = "4 HZ",command =  lambda: self.set_freq(3))
        self.freq.add_command(label = "8 HZ",command =  lambda: self.set_freq(4))
        self.freq.add_command(label = "16 HZ",command =  lambda: self.set_freq(5))
        self.bars["About"].add_command(label = "Info", command = self.pop_info)

        self.sym = {}





    def get_text(self):
        text = ""
        return text



    def save(self):

        self.text =self.get_text()

        #change path
        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) +"/Files"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        #create file
        self.fileName =time.strftime("%d-%m-%y_%H-%M-%S",time.localtime())+".txt"
        self.f = open(self.fileName,"w")
        self.f.write(self.text)
        self.f.close()



    def pop_load(self):

        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) +"/Files"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        self.popLoad = Toplevel()
        self.popLoad.title("Load")
        v = StringVar()
        self.fontSize = 12
        self.font = ("Consolas",self.fontSize)

        for (i,fileName) in enumerate(os.listdir(path)):
            Radiobutton(self.popLoad,
                        text = fileName,
                        variable =v,
                        value =fileName,
                        indicatoron = False,
                        width = 50,
                        font = self.font,
                        borderwidth = 3,
                        activeforeground = "green",
                        ).grid(row =i, column = 0)

        button =Button(self.popLoad,
                       text ="Load",
                       width= 30,
                       font = self.font,
                       borderwidth =5,
                       command = lambda:self.load(v.get())
                       )
        button.grid(row = i+1, column = 0,sticky ="n")
        self.popLoad.mainloop()


    def load(self,fileName):
        path = os.path.abspath("")
        dir_path = os.path.dirname(os.path.realpath(__file__)) +"/Files"
        os.chdir(dir_path)
        path = os.path.abspath("./")

        self.fileName = fileName
        self.f = open(self.fileName,"r")
        self.fileContent = self.f.read()
        self.writeText(self.fileContent)
        self.popLoad.destroy()
        self.reset()

    def writeText(self,text):
        self.text =text

    def reset(self):

        pass





    def set_freq(self, freq):

        pass

    def update_sym(self,sym):
        self.sym = sym


    def pop_symbol(self):  #passing in a func from display in main


        keyList = list(self.sym.keys())
        valList = list(self.sym.values())

        top = Toplevel()
        top.title("Symbol Table")
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        top.columnconfigure(1,weight=1)
        labName = Label(top,text="Label Names",font=("Consolas",23),bd=1,relief="solid",anchor=CENTER,justify=CENTER)
        labName.grid(row=0,column=0,sticky=N+S)
        address = Label(top,text="Addresses",font=("Consolas",23),bd=1,relief="solid",anchor=CENTER,justify=CENTER)
        address.grid(row=0,column=1,sticky=N+S)
        r = 1
        for i in range(len(keyList)):
            keyLab = Label(top,text=keyList[i],bd=1,relief="solid",font=("Consolas",18),anchor=CENTER,justify=CENTER)
            keyLab.grid(row=r,column=0,sticky=N+E+S+W)
            valLab = Label(top,text=valList[i],bd=1,relief="solid",font=("Consolas",18),anchor=CENTER,justify=CENTER)
            valLab.grid(row=r,column=1,sticky=N+E+S+W)
            r += 1

        pass

    def assign_numSys(self,func):
        self.set_numSys = func
        pass

    def setVersion(self,ver):
        self.verStr = ver

    def pop_info(self):
        popup = Toplevel()
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
        ("Tanthun Assawapitiyaporn - Just a random and lonely boi",font2),
        ("Martin Lee - Head of programming",font2),
        ("Version: " + self.verStr,font1)
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


    root.mainloop()
