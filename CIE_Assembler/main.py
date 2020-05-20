try:
    from Tkinter import *
except:
    from tkinter import *
from toolbar import *
from interpreterControls import *
from editor import *
from display import *
from errorLine import *
from assembler import *
from outBar import *
from inBar import *


if __name__ == "__main__":
    root = Tk()
    root.title("CIE Assembler virtual machine")
    root.geometry("1500x800")
    root.resizable(False, False)

    asem = Assembler()
    asem.init_RAM()
    toolBar = ToolBar(root)
    editButtons = InterpreterControls(root, 0,0)
    editor = Editor(root,1,0)
    inputBar = InBar(root,3,1)
    outBar = outBar(root,2,1)
    display = Display(root, 1,1)
    errorBar = ErrorBar(root,4,1)

    #Connecting things together
    editor.report = errorBar.update
    toolBar.assign_numSys(display.numSys)
    editButtons.assign_Functions(editor.lexical_analysis, asem.passThrough, display.updateRam, errorBar.update)


    root.mainloop()
