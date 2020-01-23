try:
    from Tkinter import *
except:
    from tkinter import *

class RamDisplay:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(self.master, borderwidth = 5, relief = "groove")
        self.frame.grid(row = r, column = c)
        textArray = []
        for i in range(16):
            textArray.append([])
            for j in range(16):
                textArray[i].append(Label(self.frame, text = "00 "))
                textArray[i][j].grid(row = i, column = j)


if __name__ == "__main__":
    root = Tk()
    r = RamDisplay(root,0,0)



    root.mainloop()
