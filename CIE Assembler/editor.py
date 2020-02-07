try:
    from tkinter import *
except:
    from Tkinter import *

import tkinter.tix as Tix
import tkinter.scrolledtext as ScrolledText


class Editor:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(self.master)
        self.fontSize = 14
        self.font = ("Consolas",self.fontSize)
        self.frame.grid(row = r, column = c)
        self.textArea = ScrolledText.ScrolledText(self.frame, width = 40, height = 20, font = self.font)
        self.textArea.Text.configure(text = "enter your text")
        self.textArea.grid(row = 0, column = 1)


    def check_syntax(self):


        return 1

    def lexical_analysis(self):





        return





if __name__ == "__main__":
    root = Tk()
    editor = Editor(root,0,0)



    root.mainloop()
