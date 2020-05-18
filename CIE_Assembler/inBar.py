try:
    from Tkinter import *
except:
    from tkinter import *


class InBar:
    def __init__(self, master, r, c):
        self.master = master
        self.labelFrame = Frame(master)
        self.labelFrame.grid(row = r, column = c)
        self.label = Label(self.labelFrame,text="Input:")
        self.label.grid(row = 0, column = 0)
        self.entryFrame = Frame(master)
        self.entryFrame.grid(row = r, column = c + 1)
        self.entry = Entry(self.entryFrame)
        self.entry.grid(row = 0, column = 0)



if __name__ == "__main__":
    root = Tk()
    inBar = InBar(root,0,0)
    root.mainloop()
