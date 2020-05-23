try:
    from Tkinter import *
except:
    from tkinter import *


class InBar:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(master,borderwidth=5,relief="groove", bg = "white")
        self.frame.grid(row=r, column=c, sticky = W)
        self.fontSize = 12
        self.font = ("Consolas",self.fontSize)
        self.label = Label(self.frame,text="Input: ",font=self.font,width=8, bg = "white")
        self.label.grid(row=0, column=0)
        self.strVar = StringVar()
        self.entry = Entry(self.frame,textvariable=self.strVar,width=10,justify=LEFT, font = self.font,state = "disabled", bg ="white")
        self.entry.grid(row=0, column=1)
        #self.enterButton = Button(self.frame,text="Enter",font=self.font,width=7,command=self.enterInput)
        #self.enterButton.grid(row=0,column=2)

    def passInput(self,input):  #stub function for syntax.py
        pass

    def enterInput(self):
        input = self.strVar.get()
        print(input)
        self.passInput(input)   #stub function



if __name__ == "__main__":
    root = Tk()
    inBar = InBar(root,0,0)
    inBar.enterInput()
    root.mainloop()
