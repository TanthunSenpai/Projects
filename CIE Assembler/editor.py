try:
    from tkinter import *
except:
    from Tkinter import *


class Editor:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(self.master)
        self.fontSize = 14
        self.font = ("Consolas",self.fontSize)
        self.frame.grid(row = r, column = c)
        self.scrollBar = Scrollbar(self.frame, orient = VERTICAL)
        self.scrollBar.pack(side = RIGHT, fill = Y)
        self.textArea = Text(self.frame, width = 40, height = 20, font = self.font, yscrollcommand = self.scrollBar.set)
        self.textArea.pack(side = LEFT)
        self.scrollBar.config(command = self.textArea.yview)
        self.textArea.insert(INSERT, "HOOLA\n"*20)


    def check_syntax(self):


        return 1

    def lexical_analysis(self, *arg):
        text = self.textArea.get('0.0','end').strip()
        text = text.split("\n")
        print(text)



        return




if __name__ == "__main__":
    root = Tk()
    editor = Editor(root,0,0)
    editor.lexical_analysis()




    root.mainloop()
