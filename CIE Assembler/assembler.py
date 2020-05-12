#Purpose of this file: Receive tokens from front-end and turn them into opcodes (in hex) and put them in RAM

#First pass: Fix forward references and build symbol table of names, labels, and offsets, substituting tokens in place of memory locations
#Second pass: Generate machine code by converting opcodes into machine code (hex codes) and then put this into RAM
#Typically, forward references are fixed in the second pass due to variable instruction sizes (e.g. even though all instructions are 2 bytes, a few may be 3 bytes, and you'd need to account for this)

#Update: Can do everything in 1 pass, so no longer using 2 pass model

import syntax #Importing the dictionaries declared in syntax.py to be used later (may be useful, not sure yet)

class Assembler: #Writing as a class so we can have a separate class for each assembly code file.
    def __init__(self):
        self.symbolTable = [] #Structure of the symbol table will be [[label name, address in memory location]]
        self.RAM = [] #Initalises RAM by default on constructor call
        self.RAMpointer = 0 #Since RAM is modelled as a 1D list, we only need a single pointer
        #By convention, RAMpointer will point to the next available location in RAM


    def init_RAM(self): #Using a 256 byte RAM (16 by 16) in the form of a 2D list initialised to 00 in hex
        #Note: Agreed with Adi that he will have to adjust for rows by breaking into blocks of 16
        self.RAM = []
        for i in range(0,256):
            self.RAM.append("00") #Initialising each memory location to 00 in hex
        return self.RAM #Return the initialised RAM list

    def showContents(self): #TEST FUNCTION TO BE CALLED FOR DEBUG PURPOSES
        print("Current RAM state: ")
        print(self.RAM)
        print("\nSymbol Table: ")
        print(self.symbolTable)

    def label(self, line): #Note: Labels will be replaced with a hex code pointing to it's memory location in memory
        #The line passed in will be a label, followed by an opcode and an operand
        #For label case, we just place the label and it's location in memory into the symbol table
        #The rest of the label will be a regular opcode case, and so we can just add these into RAM
        label = line.pop(0)
        if label in self.symbolTable: #Means we tried jumping to it before it was defined

        self.symbolTable.append([]) #Appends a row to the symbol table so we can add our label and position in RAM
        self.symbolTable[len(self.symbolTable) - 1].append(line)
        hexLine = hex(self.RAMpointer) #Converts pointer's current position into hex
        hexLine = hexLine[2:] #Removes the 0x at the beginning of the hex number
        self.symbolTable[len(self.symbolTable) - 1].append(hexLine) #Adds label start position in RAM to the symbol table
        if len(line) == 1:
            self.specialOpcode(line)
        else:
            self.regularOpcode(line)

    def regularOpcode(self, line): #Deals with adding OPCODE OPERAND lines to RAM
        self.RAM[self.RAMpointer] = syntax.OPCODETOHEXDICT[line[0]] # First part will always be an opcode
        self.RAMpointer += 1
        if line[1] in syntax.SPECIALOPERANDS: #Checking if the original line was in the form OPCODE SPECIALOPERAND
            self.RAM[self.RAMpointer] = syntax.SPECIALOPERANDS[line[1]]
        elif line[0] == "JMP": #Means the OPERAND is either an address number or a label
            try:
                operand = int(line[1])
            except: #If the above failed, it must be a label operand

        else:
            self.RAM[self.RAMpointer] = hex(int(line[1]))[2:].upper() #Operand must be a number if we reached this point
            if len(self.RAM[self.RAMpointer]) == 1: #Means we should add an extra 0 at the beginning
                self.RAM[self.RAMpointer] = "0" + self.RAM[self.RAMpointer]
        self.RAMpointer += 1

    def specialOpcode(self, line): #Deals with adding OPCODE lines to RAM
        self.RAM[self.RAMpointer] = syntax.OPCODETOHEXDICT[line[0]]
        self.RAMpointer += 1

    def firstPass(self, tokenList): #Being passed a list of tokens for each line (FROM ADI)
        #Using the CIE assembly language from the 9608 specification:
        # - Labels followed by instructions will have a tuple of length 3
        # - Regular opcodes will have a length of 2
        # - Special opcodes (e.g. in, out, end) will have a length of 1

        #Purpose of firstPass is to convert the assembly code into hex, then place into RAM

        #Solving forward references approach:
        # - Start from the first token, work down until you come across a label
        # - For each token, increment the RAMpointer variable
        # - Throw the label into the symbol table and keep going until you come across where it's defined
        # - RAMpointer will hold the memory location the label would start at, so we just translate this into hex and throw this into the array

        for line in tokenList: #Iterating through the list to get each line, held as a tuple
            if len(line) == 3: #Label case
                self.label(line)
            elif len(line) == 2: #Regular opcode Case
                if line[0] not in syntax.OPCODETOHEXDICT: #Means the first part of the line is a label
                    self.label(line)
                else: #Means the line is just a regular opcode
                    self.regularOpcode(line)
            else: #Special opcode case
                self.specialOpcode(line)
    #self.secondPass()

    #def secondPass(self): #Second pass would probably be needed for "JMP" opcodes, which may jump to an undefined label




if __name__ == "__main__": #Test input for finished functions
    test = Assembler()
    test.init_RAM()
    test.firstPass([["JMP", "03"], ["LABELTHING", "END"], ["LABELNAME", "LDD", "7"]])
    test.showContents()

#Consider bus width, might be useful to model
