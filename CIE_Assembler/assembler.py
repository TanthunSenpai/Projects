#Purpose of this file: Receive tokens from front-end and turn them into opcodes (in hex) and put them in RAM

#Can do everything in 1 pass, so no longer using 2 pass model

import syntax #Importing the dictionaries declared in syntax.py to be used later

class Assembler: #Writing as a class so we can have a separate class for each assembly code file
    def __init__(self):
        self.symbolTable = {} #Structure of the symbol table will be [[label name, address in memory location]]
        self.RAM = [] #Initalises RAM by default on constructor call
        self.RAMpointer = 0 #Since RAM is modelled as a 1D list, we only need a single pointer
        #By convention, RAMpointer will point to the next available location in RAM
        self.symbolicAddress = 71 #Ascii code to be used in the case of forward references (starting from character G)
        self.allOkFlag = True #By default it is true as we assume the code is ok.
        self.errorMsg = "" #Error message to be returned after passThrough is called
        self.code = []

    def init_RAM(self): #Using a 256 byte RAM (16 by 16) in the form of a 2D list initialised to 00 in hex
        #Note: Agreed with Adi that he will have to adjust for rows by breaking into blocks of 16
        self.RAM = []
        for i in range(0,256):
            self.RAM.append("00") #Initialising each memory location to 00 in hex
        return self.RAM #Return the initialised RAM list

    def showContents(self): #TEST FUNCTION TO BE CALLED FOR DEBUGGING PURPOSES
        print("Current RAM state: ")
        print(self.RAM)
        print("\nSymbol Table: ")
        print(self.symbolTable)
        print(f"\nFunctional code flag status = {self.allOkFlag}")
        if not self.allOkFlag:
            print(f"Error message = {self.errorMsg}")

    def labelCheck(self, label, definition):
        if definition: #Method was called from a label definition line
            try:
                labelSymbol = self.symbolTable[label] #Checking if the label exists in the symbol table
            except:
                address = hex(self.RAMpointer)[2:].upper()
                if len(address) == 1:
                    address = "0" + address
                self.symbolTable[label] = address #We need to define it in the symbol table
                #The fact that this label wasn't defined means there are no symbolic addresses that we need to correct in RAM
            else:
                #We need to correct symbolic addresses in RAM as it does exist.
                address = hex(self.RAMpointer)[2:].upper()
                if len(address) == 1:
                    address = "0" + address
                self.symbolTable[label] = str(address) #Changing the symbolic address to a numerical one
                for index in range(len(self.RAM)): #Iterating through RAM to find where the symbolic address is used
                    if self.RAM[index] == labelSymbol: #True means we have found where the symbolic address is used
                        self.RAM[index] = str(address)

        else: #Not a definition, which means we need to return an address of some sort
            if label in self.symbolTable: #Checking if the label exists in the symbol table
                return self.symbolTable[label]
            else:
                self.symbolTable[label] = chr(self.symbolicAddress) #Defining the label with a symbolic address for now
                self.symbolicAddress += 1
                return self.symbolTable[label]

    def label(self, line): #Note: Labels will be replaced with a hex code pointing to it's memory location in memory
        #The line passed in will be a label, followed by an opcode and/or an operand
        #For label case, we just place the label and it's location in memory into the symbol table
        #The rest of the label will be a regular or special opcode case, and so we can just add these into RAM
        label = line.pop(0)
        self.labelCheck(label, True)
        if len(line) == 1:
            self.specialOpcode(line)
        else:
            self.regularOpcode(line)

    def regularOpcode(self, line): #Deals with adding OPCODE OPERAND (operand can be number, specialoperand or label)
        self.RAM[self.RAMpointer] = syntax.OPCODETOHEXDICT[line[0]] # First part will always be an opcode
        self.RAMpointer += 1
        #OPCODE SPECIALOPERAND case
        #Special operands are IX and ACC
        if line[1] in syntax.SPECIALOPERANDS:
            self.RAM[self.RAMpointer] = syntax.SPECIALOPERANDS[line[1]] #If it was a special operand, we add the corresponding hex code for that operand (see syntax.py)
        #Checking between OPCODE OPERAND and OPCODE LABEL case

        #If the above was not met, then the operand must be an address or a label
        #If it's a label, we need to check if it's in the symbol table
        # - If it is, then we replace the label with the address from the symbol table
        # - If it isn't, then we add it to the symbol table with a symbolic address, which will be overwritten once the label definition is found
        #We now need to determine if the operand is an address or a label
        else:
            try:
                operand = int(line[1]) #Checking to see if the operand is a label or an address
            except: #Operand is a label
                self.RAM[self.RAMpointer] = self.labelCheck(line[1], False)
                print(self.RAM[self.RAMpointer])
                print(self.symbolTable)
            else: # JMP NUM case
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
        # - Throw the label into the symbol table with some symbol as the address, and keep going until you come across where it's defined
        # - RAMpointer will hold the memory location the label would start at, so we just translate this into hex and throw this into the array
        self.__init__()
        self.init_RAM()
        self.code = tokenList
        for line in tokenList: #Iterating through the list to get each line, held as a tuple
            if len(line) == 3: #LABEL OPCODE OPERAND
                self.label(line)
            elif len(line) == 2: #LABEL OPCODE or OPCODE OPERAND case
                if line[0] not in syntax.OPCODETOHEXDICT: #True means the first part of the line is a label
                    self.label(line) #LABEL OPCODE
                else: #False means the line is just a regular opcode
                    self.regularOpcode(line) #OPCODE OPERAND
            elif len(line) == 1: #OPCODE
                self.specialOpcode(line)
        self.errorMsg = self.checkErrors()
        return self.allOkFlag, self.RAM, self.symbolTable, self.errorMsg

    def checkErrors(self): #Function will return a string in binary to indicate what error flags have been triggered.
        # Errors possible:
        # - JMP to undefined label
        try:
            for label in self.symbolTable:
                x = int(self.symbolTable[label], 16) #Checking if all labels now have a numerical address
        except:
            self.allOkFlag = False #We need to set the flag to be false as an error has been found
            lineNo = 1
            #We now need to find what line the label is on.
            for line in self.code: #Getting each line from the code
                for item in line: #Getting each item from a line
                    if item == label: #Checking if the label matches the
                        return f"Error on line {lineNo}: {label} is undefined"
                lineNo += 1

if __name__ == "__main__": #Test input for finished functions
    test = Assembler() #Creating assembler object
    test.init_RAM() #Creating RAM
    test.passThrough([["JMP", "LABEL"], ["LABEL", "END"], [], ["JMP", "FAKELABEL"]]) #Running the assembler on this sample code
    test.showContents() #Debug function to see output

#Consider bus width, might be useful to model?
