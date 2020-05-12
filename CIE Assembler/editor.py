try:
    from tkinter import *
except:
    from Tkinter import *

import syntax
import random

cheerMessages = ["Amazing! you have no errors, I am surprised",
                "Great!",
                "FINALLY",
                "It took you a long time, but you did it",
                "I didn't know you are capable of writing errorless code",
                "Good Job!",
                "AHahahahhahaha",
                "I doubt you understood what you did, but anyway Good Job!",
                "Nice!",
                "Is it bird!?.. Is it an airplane!?... Is it a Glider!?...NO! it's a code without mistakes..."
                ]


def check_syntax(token_list):
    for i,line in enumerate(token_list):
        if len(line) > 3:
            return False, i+1, "too many words in a line"



    return True, "", random.choice(cheerMessages)




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
        self.textArea = Text(self.frame,
                            width=40,
                            height=25,
                            font=self.font,
                            yscrollcommand=self.scrollBar.set
                            )
        self.textArea.pack(side=LEFT)
        self.scrollBar.config(command=self.textArea.yview)
        self.textArea.insert(INSERT, "Write your text here my friend...")


    def lexical_analysis(self):
        text = self.textArea.get('0.0', 'end').strip()
        text = text.split("\n")
        ret = []

        for line in text:
            ret.append(line.strip().split())
        is_valid, linNo, msg = check_syntax(ret)
        if not is_valid:
            self.rep("Oopsie on line:" + str(linNo) + "|errorCode: " + msg)
        else:
            self.rep("No error: " + msg)

        return ret


if __name__ == "__main__":
    root = Tk()
    editor = Editor(root, 0, 0)


    root.mainloop()
