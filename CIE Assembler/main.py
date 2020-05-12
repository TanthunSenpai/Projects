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
    display = Display(root, 1,2)
    errorBar = ErrorBar(root,3,0)
    editor.rep = errorBar.update
    toolBar.assign_numSys(display.numSys)
    editButtons.assign_Functions(editor.lexical_analysis, asem.passThrough, display.updateRam)



    root.mainloop()
