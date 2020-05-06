#Purpose of this file: Receive tokens from front-end and turn them into opcodes (in hex) and put them in RAM

#First pass: Fix forward references and build symbol table of names, labels, and offsets, substituting tokens in place of memory locations
#Second pass: Generate machine code by converting opcodes into machine code (hex codes) and then put this into RAM
#Typically, forward references are fixed in the second pass due to variable instruction sizes (e.g. even though all instructions are 2 bytes, a few may be 3 bytes, and you'd need to account for this)

#Update: Can do everything in 1 pass, so no longer using 2 pass model

#from syntax import * #Importing the dictionaries declared in syntax.py to be used later (may be useful, not sure yet)

class Assembler:
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

    def showContents(self): #TEST FUNCTION TO BE REMOVED LATER
        print("Current RAM state: ")
        print(self.RAM)
        print("\nSymbol Table: ")
        print(self.symbolTable)

    def label(self, line): #Note: Labels will be replaced with a hex code pointing to it's memory location in memory
        #The line passed in will be a label, followed by an opcode and an operand
        #For label case, we just place the label and it's location in memory into the symbol table
        #The rest of the label will be a regular opcode case, and so we can just add these into RAM
        self.symbolTable.append([]) #Appends a row to the symbol table so we can add our label and position in RAM
        self.symbolTable[len(self.symbolTable) - 1].append(line[0])
        hexLine = hex(self.RAMpointer)
        hexLine = hexLine[2:] #Removes the 0x at the beginning of the hex number
        self.symbolTable[len(self.symbolTable) - 1].append(hexLine)
        self.RAM[self.RAMpointer] = line[1] #Opcode
        self.RAMpointer += 1
        self.RAM[self.RAMpointer] = line[2] #Operand
        self.RAMpointer += 1


    def regularOpcode(self, line):
        self.RAM[self.RAMpointer] = line[1] #Opcode
        self.RAMpointer += 1
        self.RAM[self.RAMpointer] = line[2] #Operand
        self.RAMpointer += 1

    def specialOpcode(self, line): #TBF
        return

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

        for item in tokenList: #Iterating through the list to get each line, held as a tuple
            if len(item) == 3: #Label case
                self.label(item)
            elif len(item) == 2: #Opcode Case
                self.regularOpcode(item)
            else: #Special case
                self.specialOpcode(item)




if __name__ == "__main__": #Test input for finished functions
    test = Assembler()
    test.init_RAM()
    test.firstPass([["LABELNAME", "LDD", "7"]])
    test.showContents()

#Consider bus width, might be useful to model
