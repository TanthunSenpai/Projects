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
    VERSION = "0.1"
    root = Tk()
    root.title("CIE Assembler virtual machine")
    root.geometry("1500x800")
    root.resizable(False, False)

    asem = Assembler()
    asem.init_RAM()
    toolBar = ToolBar(root)
    editButtons = InterpreterControls(root,0,0)
    displayFrame = Frame(root)
    displayFrame.grid(row = 1, column = 1)
    editor = Editor(root,1,0)
    inputBar = InBar(displayFrame,2,0)
    outBar = outBar(displayFrame,1,0)
    display = Display(displayFrame,0,0)
    errorBar = ErrorBar(displayFrame,3,0)


    #Connecting things together
    editor.report = errorBar.update
    toolBar.setVersion(VERSION)
    toolBar.assign_numSys(display.numSys)

    editButtons.update_sym = toolBar.update_sym
    inStub = inputBar.passInput
    outStub = outBar.out

    editButtons.assign_Functions(editor.lexical_analysis, asem.passThrough, display.updateArgs, errorBar.update)
    toolBar.get_text = editor.get_text
    toolBar.writeText = editor.insert_text

    root.mainloop()
