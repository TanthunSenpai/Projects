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
    args["ACC"] = args["RAM"][args["PC"]+1]
    args["PC"] += 2

def LDD(args):
    addrss = args["RAM"][args["PC"]+1]
    args["ACC"] = args["RAM"][addrss]
    args["PC"] += 2

def LDI(args):
    addrss = args["RAM"][args["PC"]+1]
    value = args["RAM"][addrss]
    args["ACC"] = value
    args["PC"] += 2

def LDX(args):
    addrss = args["RAM"][args["PC"]+1]
    newAddrss = addrss + args["IX"]
    args["ACC"] = args["RAM"][newAddrss]
    args["PC"] += 2

def LDR(args):
    args["IX"] = args["RAM"][args["PC"]+1]
    args["PC"] += 2

def STO(args):
    args["RAM"][args["PC"]+1] = args["ACC"]
    args["PC"] += 2

def ADD(args):
    args["ACC"] += args["RAM"][args["PC"]+1]
    args["PC"] += 2

def INC(args):
    if args["RAM"][args["PC"]+1] == "EE":
        args["ACC"] += 1
    elif args["RAM"][args["PC"]+1] == "FF":
        args["IX"] += 1
    else:
        args["halt"] = True
        args["errorMsg"] = "Register error: operand is not ACC or IX."
    args["PC"] += 2

def DEC(args):
    if args["RAM"][args["PC"]+1] == "EE":
        args["ACC"] -= 1
    elif args["RAM"][args["PC"]+1] == "FF":
        args["IX"] -= 1
    else:
        args["halt"] = True
        args["errorMsg"] = "Register error: only ACC and IX can be decremented."
    args["PC"] += 2

def JMP(args):
    args["PC"] = args["RAM"][args["PC"]+1]

def CMP(args):  #format: CMP ADDRESSINGMODE OPERAND
    args["ZMP"] = True
    if args["RAM"][args["PC"]+1] == 0:  #immediate addressing mode
        num = args["RAM"][args["PC"]+2]
        if num == args["ACC"]:
            args["ZMP"] = True
        else:
            args["ZMP"] = False

    elif args["RAM"][args["PC"]+1] == 1:   #direct addressing mode
        addrss = args["RAM"][args["PC"]+2]
        if args["RAM"][addrss] == args["ACC"]:
            args["ZMP"] = True
        else:
            args["ZMP"] = False
    else:   #neither immediate nor direct addressing modes
        args["halt"] = True
        args["errorMsg"] = "Addressing mode error: only immediate or direct addressing modes are allowed"
    args["PC"] += 3

def JPE(args):
    addrss = args["RAM"][args["PC"]+1]
    if args["ZMP"] == True:   #they are equal
        args["PC"] = addrss
    else:   #they are not equal, continue the execution without jumping
        args["PC"] += 2

def JPN(args):
    addrss = args["RAM"][args["PC"]+1]
    if args["ZMP"] == False:  #they are not equal
        args["PC"] = addrss
    else:   #they are equal, continue the execution without jumping
        args["PC"] += 2

def inStub(chrcter):
    return chrcter

def IN(args):
    chrcter = inStub(chrcter)
    args["ACC"] = ord(chrcter)
    args["PC"] += 1

def outStub(chrcter):
    pass

def OUT(args):
    chrcter = chr(args["ACC"])
    outStub(chrcter)
    args["PC"] += 1

def END(args):
    print(args["ACC"])
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
