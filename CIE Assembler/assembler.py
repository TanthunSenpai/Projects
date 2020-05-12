#Purpose of this file: Receive tokens from front-end and turn them into opcodes (in hex) and put them in RAM

#First pass: Fix forward references and build symbol table of names, labels, and offsets, substituting tokens in place of memory locations
#Second pass: Generate machine code by converting opcodes into machine code (hex codes) and then put this into RAM
#Typically, forward references are fixed in the second pass due to variable instruction sizes (e.g. even though all instructions are 2 bytes, a few may be 3 bytes, and you'd need to account for this)

#Update: Can do everything in 1 pass, so no longer using 2 pass model

import syntax #Importing the dictionaries declared in syntax.py to be used later (may be useful, not sure yet)

class Assembler: #Writing as a class so we can have a separate class for each assembly code file.
    def __init__(self):
        self.symbolTable = {} #Structure of the symbol table will be [[label name, address in memory location]]
        self.RAM = [] #Initalises RAM by default on constructor call
        self.RAMpointer = 0 #Since RAM is modelled as a 1D list, we only need a single pointer
        #By convention, RAMpointer will point to the next available location in RAM
        self.symbol = 71 #Ascii code to be used in the case of forward references (starting from character G)


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
        exists = False #Temporary variable to check if the label exists in the symbol table
        for item in self.symbolTable:
            if label == item: #Means we tried jumping to it before it was defined, hence why it exists in the symbolTable beforehand
                exists = True
        if exists == True: #Means the label is in the symbol table, so we have to set it's pointer to the current RAMpointer, then change the symbol in RAM
            for index in range(len(self.RAM)): #Iterating through RAM to find where the JMP opcodes are
                if self.RAM[index] == syntax.OPCODETOHEXDICT["JMP"]:
                    if self.RAM[index + 1] == self.symbolTable[label]: #True evaluation means this JMP instruction corresponds to this label
                        pointerToAdd = hex(self.RAMpointer)[2:].upper()
                        if len(pointerToAdd) == 1:
                            pointerToAdd = "0" + pointerToAdd
                        self.RAM[index + 1] = pointerToAdd #Changing RAM symbol to the pointer
                        self.symbolTable[label] = pointerToAdd #Changing the symbol in the symbolTable to the pointer
                        #We can't add a break here as there may be multiple jumps to the same label in the code, so we need to check everything!
        else: #Means the label doesn't exist in the symbol table currently
            hexLine = hex(self.RAMpointer)[2:].upper()#Converts pointer's current position into hex
            if len(hexLine) == 1:
                hexLine = "0" + hexLine
            self.symbolTable[label] = hexLine #Adds label start position in RAM to the symbol table

        if len(line) == 1:
            self.specialOpcode(line)
        else:
            self.regularOpcode(line)

    def regularOpcode(self, line): #Deals with adding OPCODE OPERAND lines to RAM
        self.RAM[self.RAMpointer] = syntax.OPCODETOHEXDICT[line[0]] # First part will always be an opcode
        self.RAMpointer += 1
        if line[1] in syntax.SPECIALOPERANDS: #Checking if the original line was in the form OPCODE SPECIALOPERAND
            self.RAM[self.RAMpointer] = syntax.SPECIALOPERANDS[line[1]] #If it was a specal operand, we add the corresponding hex code for that operand (see syntax.py)
        elif line[0] == "JMP": #Means the OPERAND is either an address number or a label
            try:
                operand = int(line[1]) #Checking to see if the operand is a number
            except: #If the above failed, it must be a label operand
                pointerExists = False
                for row in self.symbolTable:
                    if row == line[1]: #Means our label has been defined before this JMP opcode, and so it exists
                        pointerExists = True
                        pointerToAdd = self.symbolTable[line[1]] #Assigns the current label's pointer to the table
                if pointerExists:
                    self.RAM[self.RAMpointer] = pointerToAdd
                else: #Means the label doesn't exist in the symbol table, and so we need to add it.
                    self.RAM[self.RAMpointer] = chr(self.symbol) #Adding symbol to RAM instead
                    self.symbolTable[line[1]] = chr(self.symbol) #Assigning JMP operand i.e. the label to the symbol
                    self.symbol += 1 #Changing to next symbol code
            else: #Case of JMP operand being a number
                self.RAM[self.RAMpointer] = hex(int(line[1]))[2:].upper() #Operand must be a number if we reached this point
                if len(self.RAM[self.RAMpointer]) == 1: #Means we should add an extra 0 at the beginning
                    self.RAM[self.RAMpointer] = "0" + self.RAM[self.RAMpointer]
        else: #Means it wasn't a special operand or a JMP opcode, so we just have a regular number
            self.RAM[self.RAMpointer] = hex(int(line[1]))[2:].upper() #Operand must be a number if we reached this point
            if len(self.RAM[self.RAMpointer]) == 1: #Means we should add an extra 0 at the beginning
                self.RAM[self.RAMpointer] = "0" + self.RAM[self.RAMpointer]
        self.RAMpointer += 1

    def specialOpcode(self, line): #Deals with adding OPCODE lines to RAM
        self.RAM[self.RAMpointer] = syntax.OPCODETOHEXDICT[line[0]]
        self.RAMpointer += 1

    def passThrough(self, tokenList): #Being passed a list of tokens for each line (FROM ADI)
        #Using the CIE assembly language from the 9608 specification:
        # - Labels followed by instructions will have a tuple of length 3
        # - Regular opcodes will have a length of 2
        # - Special opcodes (e.g. in, out, end) will have a length of 1
        # - By convention, labels must have opcodes after them! They can't be blank
        #Purpose of passThrough is to convert the assembly code into hex, then place into RAM

        #Solving forward references approach:
        # - Start from the first token, work down until you come across a label
        # - For each token, increment the RAMpointer variable
        # - Throw the label into the symbol table and keep going until you come across where it's defined
        # - RAMpointer will hold the memory location the label would start at, so we just translate this into hex and throw this into the array
        self.__init__()
        self.init_RAM()
        for line in tokenList: #Iterating through the list to get each line, held as a tuple
            if len(line) == 3: #Label case
                self.label(line)
            elif len(line) == 2: #Regular opcode case
                if line[0] not in syntax.OPCODETOHEXDICT: #Means the first part of the line is a label
                    self.label(line)
                else: #Means the line is just a regular opcode
                    self.regularOpcode(line)
            else: #Special opcode case
                self.specialOpcode(line)
        return self.RAM, self.symbolTable



if __name__ == "__main__": #Test input for finished functions
    test = Assembler() #Creating assembler object
    test.init_RAM() #Creating RAM
    test.passThrough([["JMP", "OTHERLABEL"],["LDD","174"],["LDD","174"],["LDD","174"],["LDD","174"],["OUT"],["LABELNAME", "END"],["OTHERLABEL", "LDM","252"]]) #Running the assembler on this sample code
    test.showContents() #Debug function to see output

#Consider bus width, might be useful to model
