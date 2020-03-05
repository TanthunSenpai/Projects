#Purpose of this file: Receive tokens from front-end and turn them into opcodes (in hex) and put them in RAM

#First pass: Fix forward references and build symbol table of names, labels, and offsets, substituting tokens in place of memory locations
#Second pass: Generate machine code by converting opcodes into machine code (hex codes) and then put this into RAM
#Typically, forward references are fixed in the second pass due to variable instruction sizes (e.g. even though all instructions are 2 bytes, a few may be 3 bytes, and you'd need to account for this)

from syntax import * #Importing the dictionaries declared in syntax.py to be used later

class Assembler:
    def __init__(self):
        self.symbolTable = [] #Structure of the symbol table will be [[label name, address in memory location]]
        self.lineCount = 0 #To count the lines as we parse them (helps with accounting for forward references)
        self.RAM = []
        self.RAMpointer = 0


    def init_RAM(self): #Using a 256 byte RAM (16 by 16) in the form of a 2D list initialised to 00 in hex
        self.RAM = []
        return self.RAM #Return the initialised RAM list

    def inc_RAMpointers():

    def label(self, line): #Note: Labels will be replaced with a hex code pointing to it's memory location in memory
        #The line passed in will be a label, followed by an opcode and an operand
        self.symbolTable.append([])
        self.symbolTable[len(self.symbolTable) - 1].append(line[0])
        hexLine = hex(self.lineCount)
        hexLine = hexLine[2:] #Converts the line number into a hex number
        self.symbolTable[len(self.symbolTable) - 1].append(hexLine)
        self.RAM[self.RAMpointer] = line[1]
        self.RAMpointer += 1
        self.RAM[self.RAMpointer] = line[2]


    def regularOpcode(self, line): #TBF
        return

    def specialOpcode(self, line): #TBF
        return

    def firstPass(self, tokenList, RAM): #Being passed a list of tokens for each line (FROM ADI), and the current state of RAM
        #TBF
        #Using the CIE assembly language from the 9608 specification:
        # - Labels followed by instructions will have a tuple of length 3
        # - Regular opcodes will have a length of 2
        # - Special opcodes (e.g. in, out, end) will have a length of 1

        #Solving forward references approach:
        # - Start from the first token, work down until you come across a label
        # - For each token, increment the lineCount variable
        # - Throw the label into the symbol table and keep going until you come across where it's defined
        # - The lineCount counter will hold the memory location the label would start at, so we just translate this into hex and throw this into the array

        for item in tokenList: #Iterating through the list to get each line, held as a tuple
            if len(item) == 3: #Label case
                label(item)
            elif len(item) == 2: #Opcode Case
                regularOpcode(item)
            else: #Special case
                specialOpcode(item)




if __name__ == "__main__":
    print(init_RAM())

#Consider bus width, might be useful to model
