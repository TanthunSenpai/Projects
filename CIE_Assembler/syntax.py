OPCODETOHEXDICT = {  # CONSTANT Dictionary to hold keywords and functions that will be called
    "LDM": "0A",
    "LDD": "0B",
    "LDI": "0C",
    "LDX": "0D",
    "LDR": "0E",
    "STO": "0F",
    "ADD": "1A",
    "INC": "1B",
    "DEC": "1C",
    "JMP": "1D",
    "CMP": "1E",
    "JPE": "1F",
    "JPN": "2A",
    "IN": "2B",
    "OUT": "2C",
    "END": "2D"
}

SPECIALOPERANDS = {
    "ACC": "EE",
    "IX": "FF"
}


"""
"RAM" = [ , , ,ldd ,100 , , , , , , , , ]
             ^
             pc
!!!
EVERYTHING IN "RAM" IS IN HEX
!!!

interpreter:
    looks at "RAM"["PC"]
    and calls the method

# dictionary that is passed to all functions
args = {
    "PC" - int
    "RAM" - a list
    "ACC" - int
    "IX" - int
    "ZMP" - bool - comparison flag: equal(True), not equal(False)
    "halt" - bool - halt flag
    "errorMsg" - string - execution result - default: execution successful
}

[   , , , , , inc, 12, , , sto, ,jmp ]

def stubFunc(args):
    -update pc
    (in ldd case pc+= 2)
    -do stuff
    (in ldd case:)
    registers["EE"] = "RAM"[int("RAM"[pc+1], 16)]
"""

def LDM(args):
    args["ACC"] = int(str(strargs["RAM"][(args["PC"]+1)%256]),16)
    args["PC"] = (args["PC"] + 2) % 256

def LDD(args):
    addrss = int(str(args["RAM"][(args["PC"]+1)%256]),10)
    args["ACC"] = int(str(args["RAM"][addrss]),16)
    args["PC"] = (args["PC"] + 2) % 256

def LDI(args):
    addrss = int(str(args["RAM"][(args["PC"]+1)%256]),10)
    value = str(args["RAM"][addrss])
    args["ACC"] = int(value,16)
    args["PC"] = (args["PC"] + 2) % 256

def LDX(args):
    addrss = int((args["RAM"][(args["PC"]+1)%256]),10)
    newAddrss = addrss + int(str(args["IX"]),10)
    args["ACC"] = int(str(args["RAM"][newAddrss]),16)
    args["PC"] = (args["PC"] + 2) % 256

def LDR(args):
    args["IX"] = int(str(args["RAM"][(args["PC"]+1)%256]),16)
    args["PC"] = (args["PC"] + 2) % 256

def STO(args):
    args["RAM"][(args["PC"]+1)%256] = int(str(args["ACC"]),16)
    args["PC"] = (args["PC"] + 2) % 256

def ADD(args):
    args["ACC"] = int(str(args["RAM"][(args["PC"]+1)%256]),16)
    args["PC"] = (args["PC"] + 2) % 256

def INC(args):
    if args["RAM"][(args["PC"]+1)%256] == "EE":
        args["ACC"] = int(str(int(str(args["ACC"]),10) + 1),16) #change ACC from hex to denary for increment then back to hex
    elif args["RAM"][(args["PC"]+1)%256] == "FF":
        args["IX"] = int(str(int(str(args["ACC"]),10) + 1) 16)  #change IX from hex to denary for increment then back to hex
    else:
        args["halt"] = True
        args["errorMsg"] = "Register error: register is not ACC or IX."
    args["PC"] = (args["PC"] + 2) % 256

def DEC(args):
    if args["RAM"][(args["PC"]+1)%256] == "EE":
        args["ACC"] = int(str(int(str(args["ACC"]),10) 0 1),16) #change ACC from hex to denar for decrement then back to hex
    elif args["RAM"][(args["PC"]+1)%256] == "FF":
        args["IX"] = int(str(int(str(args["ACC"]),10) + 1) 16)  #change IX from hex to denary for decrement then back to hex
    else:
        args["halt"] = True
        args["errorMsg"] = "Register error: register is not ACC or IX."
    args["PC"] = (args["PC"] + 2) % 256

def JMP(args):
    args["PC"] = int(str(args["RAM"][(args["PC"]+1)%256]),10)   #change hex address to denary for PC

def CMP(args):  #format: CMP ADDRESSINGMODE OPERAND
    args["ZMP"] = True
    if int(args["RAM"][(args["PC"]+1)%256]) == 0:  #immediate addressing mode
        num = int(str(args["RAM"][args["PC"]+2]),16)    #num is in hex
        if num == args["ACC"]:
            args["ZMP"] = True
        else:
            args["ZMP"] = False

    elif int(args["RAM"][(args["PC"]+1)%256]) == 1:   #direct addressing mode
        addrss = int(str(args["RAM"][args["PC"]+2]),10) #change hex address to denary
        if int(str(args["RAM"][addrss]),16) == args["ACC"]: #both numbers are in hex
            args["ZMP"] = True
        else:
            args["ZMP"] = False
    else:   #neither immediate nor direct addressing modes
        args["halt"] = True
        args["errorMsg"] = "Addressing mode error: only immediate or direct addressing modes are allowed"
    args["PC"] = (args["PC"] + 3) % 256

def JPE(args):
    addrss = int(str(args["RAM"][(args["PC"]+1)%256]),10)
    if args["ZMP"] == True:   #case: equal
        args["PC"] = addrss #in denary, PC is a pointer
    else:   #case: not equal, continue.
        args["PC"] = (args["PC"] + 2) % 256

def JPN(args):
    addrss = int(str(args["RAM"][(args["PC"]+1)%256]),10)
    if args["ZMP"] == False:  #case: not equal
        args["PC"] = addrss #in denary, PC is a pointer
    else:   #case: equal, continue.
        args["PC"] = (args["PC"] + 2) % 256

def inStub(chrcter):
    return chrcter

def IN(args):
    chrcter = inStub(chrcter)
    args["ACC"] = int(str(ord(chrcter)),16) #convert ASCII to denary to hex
    args["PC"] = (args["PC"] + 1) % 256

def outStub(chrcter):
    pass

def OUT(args):
    chrcter = chr(int(str(args["ACC"]),10)) #convert hex number to denary to ASCII
    outStub(chrcter)
    args["PC"] = (args["PC"] + 1) % 256

def END(args):
    pass

HEXTOFUNCTIONDICT = {
    "0A": LDM,
    "0B": LDD,
    "0C": LDI,
    "0D": LDX,
    "0E": LDR,
    "0F": STO,
    "1A": ADD,
    "1B": INC,
    "1C": DEC,
    "1D": JMP,
    "1E": CMP,
    "1F": JPE,
    "2A": JPN,
    "2B": IN,
    "2C": OUT,
    "2D": END
}
