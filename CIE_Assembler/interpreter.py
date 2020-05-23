import syntax #Needed to access the HEXTOFUNCTIONDICT dictionary

class Interpreter:
    def __init__(self, currentRAM, master, runFreq):
        self.master = master
        self.runFreq = runFreq
        self.args = { #Dictionary that holds all arguments needed
            "PC": 0, #Program counter
            "RAM": currentRAM, #State of RAM
            "ACC": 0, #Accumulator
            "IX": 0, #Index register
            "ZMP": False, #Comparison flag
            "halt": False, #Halt flag
            "errorMsg": "Execution successful" #Error message to be given out in the case of a flag
            }

    def execute(stepFlag):
        syntax.HEXTOFUNCTIONDICT[self.args["RAM"][self.args["PC"]]](self.args) #Calls the respective method for the opcode that the PC is pointing at, passing the dictionary in as a parameter
        if not (self.args["halt"] or stepFlag) or self.args["PC"] > 255: #Checking if we can schedule the next call to execute
            self.master.after(self.runFreq, lambda: self.execute(stepFlag))
        return self.args #We return the dictionary for adi to display the error message

    def updateArgs(): #Stub function which will be overwritten by Adi's updateArgs method
        print(self.args)

    def stop(): #Method to be called in the event that the stop button is pressed
        self.args["halt"] = True

    def start(stepFlag): #Method to run code if code has been stopped halfway through. Can also be used if mode is changed from step to run.
        if self.args["PC"] > 255:
            self.args["errorMsg"] = "Cannot run code: Pointer has reached end of memory."
            return self.args
        else:
            self.execute(stepFlag)

if __name__ == "__main__": #Debug code
    import assembler
    test = Assembler() #Creating assembler object
    test.init_RAM() #Creating RAM
    allOkFlag, RAM, symbolTable, errorMsg = test.passThrough([["JMP", "LABEL"], ["LABEL", "END"], ["CMP", "#16"], ["JMP", "FAKELABEL"]]) #Running the assembler on this sample code
    interpreter = Interpreter(RAM)
    interpreter.execute()



"""PLAN:

class Interpreter:
    constructor(RAM, symbolTable):
        self.RAM = RAM
        self.symbolTable = symbolTable
        self.PC = 0
        self.registers = {
            "EE": 0, #ACC
            "FF": 0  #IX
        }
        self.haltFlag = False

    executeMethod():
        self.RAM, self.PC, self.registers, self.haltFlag = HEXTOFUNCTIONDICT[self.RAM[self.PC]](self.PC, self.RAM, self.registers) #We call the syntax.py methods, which return RAM, PC and registers
        return self.RAM, self.PC, self.registers, self.haltFlag #This gets returned to whatever called it so it can be displayed




#Not sure where this method would go so here's a rough plan of what I'm thinking

Put this in main

interpreter = Interpreter(RAM, symbolTable) #Creating interpreter object here
haltFlag = False


interpretMethod(stepFlag):
    RAM, PC, registers, haltFlag = interpreter.executeMethod()
    if not(stepFlag): #We can by default have some step flag which indicates if we are stepping or not
        #SCHEDULE CALL HERE

"""
