try:
    from Tkinter import *
except:
    from tkinter import *
from toolbar import *
from editorButtons import *


if __name__ == "__main__":
    root = Tk()
    root.title("CIE Assembler virtual machine")
    root.geometry("600x600")

    toolBar = ToolBar(root)
    editButtons = EditorButtons(root, 0,0)






    root.mainloop()
