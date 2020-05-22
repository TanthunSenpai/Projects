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
                "Is it a bird!?.. Is it an airplane!?... Is it a Glider!?...NO! it's a code without mistakes...",
                "You should be proud of your self",
                "No syntax errors doesn't mean your code is any good",
                "WOW NO ERRORS! HOW DID YOU DO THAT?"
                ]




def is_valid_operand(s):
    valid = True
    if len(s) > 3:
        valid = False
    return valid


class Editor:
    def __init__(self, master, r, c):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.grid(row=r, column=c)
        self.fontSize = 14
        self.font = ("Consolas", self.fontSize)
        self.lineList = [1]

        self.scrollBar = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.scrollBar.config(command =self.yview)
        self.numLine = Listbox(self.frame,
                               width = 3,
                               height= 25,
                               font = self.font,
                               yscrollcommand =self.scrollBar.set
                               )
        self.numLine.pack(side = LEFT)

        self.textArea = Text(self.frame,
                            width=40,
                            height=25,
                            font=self.font,
                            yscrollcommand=self.scrollBar.set,
                            spacing1 =1
                            )
        self.textArea.pack(side=LEFT)


        self.textArea.bind("<Key>",self.update_numLine)

    def yview(self, *args):
        self.numLine.yview(*args)
        self.textArea.yview(*args)


    def lexical_analysis(self):
        text = self.textArea.get('0.0', 'end').rstrip()
        text = text.split("\n")
        ret = []
        error = False
        invalid = -1

        for i, l in enumerate(text):
            line = l.strip().split()
            if line:
                for each in line:
                    if ':' in each:
                        line[line.index(each)] = "<" + each[:len(each)-1] + ">"
                    elif '#' in each and each[1:].isnumeric():
                        line[line.index(each)] = int(each[1:])
                    elif 'B' in each and each[1:].isnumeric():
                        for ch in each[1:]:
                            if int(ch) > 1:
                                self.report("Error on Line "+ str(i+1) + ": - "+ "Number is not binary")
                                return False
                        line[line.index(each)] = int(each[1:], 2)

                    elif '&' in each and each[1:].isalnum():
                        for ch in each[1:]:
                            if (ord(ch) > ord("F") or ord(ch) < ord("A")) and not ch.isnumeric():
                                self.report("Error on Line "+ str(i+1) + ": - "+ "Number is not hex")
                                return False
                        line[line.index(each)] = int(each[1:], 16)

                    elif each.isnumeric():
                        line[line.index(each)] = int(each)
                    elif not (each in syntax.OPCODETOHEXDICT or each in syntax.SPECIALOPERANDS):
                        line[line.index(each)] = "<" + each + ">"

                valid, msg = self.syntax_analysis(line)
                if not valid:
                    self.report("Error on Line "+ str(i+1) + ": - "+ msg)
                    return False

                for each in line:
                    if isinstance(each,str):
                        if each[0] == "<":
                            line[line.index(each)] = each[1:len(each)-1]

            ret.append(line)



        self.report("No error: " + random.choice(cheerMessages))
        print(ret)

        return ret


        '''
        for line in text:
            ret.append(line.strip().split())
        is_valid, linNo, msg = check_syntax(ret)
        if not is_valid:
            self.rep("Oopsie on line:" + str(linNo) + "|errorCode: " + msg)
        else:
            self.rep("No error: " + msg)

        return ret
        '''

    def syntax_analysis(self, tokens):
        opCodePos = -1
        opCodeNum = 0
        badChars = ["+","#","&" ,"-", "=", "@", "!", "$", "%", "^", "*", "(", ")", "{", "}", "[", "]", ";", "'", ".", ",", "/", '~']
        if not tokens:
            return True, None
        def inSyntax(token):
            if token in syntax.OPCODETOHEXDICT:
                return True

        if len(tokens) > 3:
            return False, "Too many words in a line"

        for token in tokens:
            if isinstance(token, str):
                if token[0] == "<" and token[-1] == ">":
                    if token[1:len(token)-1] == "B" or not token[1:len(token) -1].isalpha():
                        return False, "Bad label name"

                for char in badChars:
                    if char in token:
                        return False, "Bad character"


        for i,token in enumerate(tokens):
            if inSyntax(token):
                opCodePos = i
                opCodeNum += 1

        if opCodePos == 0 and len(tokens) > 2:
            return False, "Too many words in a line"


        if opCodeNum != 1:
            return False, "This line doesn't do anything"

        if opCodePos > 1:
            return False, "Bad opcdoe position"

        if opCodePos == 1:
            if not(tokens[0][-1] == ">" and tokens[0][1:len(tokens[0])-1].isalpha() and tokens[0][0] == "<"):
                return False, "Bad label name"



        if not tokens[opCodePos] in ["IN", "OUT", "END"]:
            if tokens[opCodePos] in ["INC", "DEC"]:
                if not tokens[opCodePos + 1] in ["ACC", "IX"]:
                    return False, "Bad operand"
            elif tokens[opCodePos] in ["LDR", "LDM", "CMP"]:
                if len(tokens) - opCodePos == 2:
                    if isinstance(tokens[opCodePos + 1], int):
                        if not(tokens[opCodePos + 1] >= 0 and tokens[opCodePos+1] < 256):
                            return False, "Number out of range"
                    else:
                        return False, "Bad Operand"
                else:
                    return False, "Empty operand"

            else:
                if len(tokens) - opCodePos == 2:
                    if isinstance(tokens[opCodePos + 1], int):
                        if not(tokens[opCodePos + 1] >= 0 and tokens[opCodePos+1] < 256):
                            return False, "Number out of range"
                else:
                    return False, "Empty operand"


        return True, None


    def get_text(self):
        text = self.textArea.get('0.0', 'end').strip()
        return text

    def insert_text(self,text):
        self.textArea.delete('0.0',END)
        self.textArea.insert('0.0', text)

    def report(self, text):
        print(text)
    """
    def update_lineList(self):
        print(self.textArea.index("end"))
        self.endLineNo = int(self.textArea.index("end")[:len(self.textArea.index("end"))-2])-1
        if self.endLineNo > max(self.lineList):
            self.lineList.append(self.endLineNo)
        elif self.endLineNo < max(self.lineList):
            self.lineList.remove(self.endLineNo+1)"""

    def update_numLine(self,event):
        #self.update_lineList()
        self.endLineNo = int(self.textArea.index("end")[:len(self.textArea.index("end"))-2])-1
        print(self.endLineNo)
        self.numLine.delete(0,END)
        for lineNum in range(self.endLineNo):
            self.numLine.insert(END,lineNum+1)





if __name__ == "__main__":
    root = Tk()
    editor = Editor(root, 0, 0)

    btn = Button(root, text = "test", command = lambda: editor.update_numLine())
    btn.grid(row = 0, column = 1)


    root.mainloop()
