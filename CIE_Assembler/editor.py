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
        self.frame = Frame(self.master, bg = "white")
        self.frame.grid(row=r, column=c)
        self.fontSize = 14
        self.font = ("Consolas", self.fontSize)
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


    def testData(self, text):
        retDict = {}
        if "<DB>" in text and "</DB>" in text:
            ptr = text.find("</DB>")
            dataText = text[:ptr+5]
            restText = text[ptr+5:]
            dataText = text[4:len(dataText) - 5]
            tokens = dataText.split("\n")
            k = -1
            for each in tokens:
                k += 1
                if each == "":
                    continue
                elif ':' in each:
                    line = each.split(":")
                    if len(line) == 2:
                        if line[0].isnumeric():
                            if line[1].isnumeric() and int(line[0]) < 256 and int(line[0]) >= 0:
                                if int(line[1]) < 256 and int(line[1]) >= 0:
                                    retDict[line[0]] = int(line[1])
                                else:
                                    return {}, text
                            else:
                                return {}, text
                        else:
                            return {}, text
                    else:
                        return {}, text
                else:
                    return {}, text

            return retDict, "\n"*k +restText
        else:
            return {}, text







    def lexical_analysis(self):
        text = self.textArea.get('0.0', 'end').rstrip()
        if text == "":
            return False, {}
        data, text = self.testData(text)
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
                        line[line.index(each)] = "<" + each[1:]
                    elif 'B' in each and each[1:].isnumeric():
                        for ch in each[1:]:
                            if int(ch) > 1:
                                self.report("Error on Line "+ str(i+1) + ": - "+ "Number is not binary")
                                return False, data
                        line[line.index(each)] = int(each[1:], 2)

                    elif '&' in each and each[1:].isalnum():
                        for ch in each[1:]:
                            if (ord(ch) > ord("F") or ord(ch) < ord("A")) and not ch.isnumeric():
                                self.report("Error on Line "+ str(i+1) + ": - "+ "Number is not hex")
                                return False, data
                        line[line.index(each)] = int(each[1:], 16)

                    elif each.isnumeric():
                        line[line.index(each)] = int(each)
                    elif not (each in syntax.OPCODETOHEXDICT or each in syntax.SPECIALOPERANDS):
                        line[line.index(each)] = "<" + each + ">"

                valid, msg = self.syntax_analysis(line)
                if not valid:
                    print(line)
                    self.report("Error on Line "+ str(i+1) + ": - "+ msg)
                    return False, data

                for each in line:
                    if isinstance(each,str):
                        if each[0] == "<":
                            line[line.index(each)] = each[1:len(each)-1]

            ret.append(line)



        self.report("No error: " + random.choice(cheerMessages))
        print(ret)
        return ret, data


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
                    if isinstance(tokens[opCodePos + 1], str):
                        if tokens[opCodePos + 1][0] == "<" and tokens[opCodePos + 1][1:].isnumeric():
                            k = int(tokens[opCodePos + 1][1:])
                            if not(k>= 0 and k < 256):
                                return False, "Number out of range"
                            if tokens[opCodePos] != "CMP":
                                tokens[opCodePos+1] = k
                            else:
                                tokens[opCodePos+1] =  "#"+tokens[opCodePos + 1][1:]

                    else:
                        if tokens[opCodePos] == "CMP":
                            print("helo")
                            if not(isinstance(tokens[opCodePos + 1], int)):
                                return False, "Bad Operand"
                            else:
                                tokens[opCodePos + 1] = str(tokens[opCodePos + 1])
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

    def update_numLine(self,event):
        self.endLineNo = int(self.textArea.index("end")[:len(self.textArea.index("end"))-2])-1
        self.numLine.delete(0,END)
        for lineNum in range(self.endLineNo):
            self.numLine.insert(END,lineNum+1)





if __name__ == "__main__":
    root = Tk()
    editor = Editor(root, 0, 0)

    btn = Button(root, text = "test", command = lambda: editor.lexical_analysis())
    btn.grid(row = 0, column = 1)


    root.mainloop()
