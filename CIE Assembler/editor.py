try:
    from tkinter import *
except:
    from Tkinter import *

import syntax


def is_valid_operand(s):
    valid = True
    if len(s) > 3:
        valid = False
    return valid


class Editor:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(self.master)
        self.fontSize = 14
        self.font = ("Consolas", self.fontSize)
        self.frame.grid(row=r, column=c)
        self.scrollBar = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.textArea = Text(self.frame, width=40, height=20,
                             font=self.font, yscrollcommand=self.scrollBar.set)
        self.textArea.pack(side=LEFT)
        self.scrollBar.config(command=self.textArea.yview)
        self.textArea.insert(INSERT, "Write your text here my friend...")

    def check_syntax(self, text):
        ret = True
        for i,line in enumerate(text):
            if len(line) > 3:
                ret = str(i) + " LINE TOO LONG"
            else:
                if len(line) == 1:
                    if line[0] != "END":
                        ret = str(i) + " IT HAS TO BE END"

                elif len(line) == 2:
                    if not(line[0] in syntax.OPCODETOHEXDICT):
                        ret = str(i) + " NOT A VALID OPCODE"

                    if not(is_valid_operand(line[1])):
                        ret = str(i) + " NOT A VALID OPERAND"

                elif len(line) == 3:
                    if line[0][-1] != ':':
                        print(line[0][-1])
                        print(':')
                        ret = str(i) + " YOU NEED :"
                    if not(line[1] in syntax.OPCODETOHEXDICT):
                        ret = str(i) + " NOT A VALID OPCODE"
                    if not(is_valid_operand(line[2])):
                        ret = str(i) + " NOT A VALID OPERAND"
        return ret



        return 1

    def lexical_analysis(self, *arg):
        text = self.textArea.get('0.0', 'end').strip()
        text = text.split("\n")
        ret = []

        for line in text:
            ret.append(line.strip().split())
        print(ret)
        print(self.check_syntax(ret))

        return ret


if __name__ == "__main__":
    root = Tk()
    editor = Editor(root, 0, 0)
    root.bind("<F5>", editor.lexical_analysis)

    root.mainloop()
