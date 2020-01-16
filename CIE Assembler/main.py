try:
    from Tkinter import *
except:
    from tkinter import *
from toolbar import *


if __name__ == "__main__":
    root = Tk()
    root.title("CIE Assembler virtual machine")
    root.geometry("600x600")

    toolBar = ToolBar(root)






    root.mainloop()
