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
ram = [ , , ,ldd ,100 , , , , , , , , ]
             ^
             pc
!!!
EVERYTHING IN RAM IS IN HEX
!!!

interpreter:
    looks at ram[pc]
    and calls the method

# dictionary that is passed to all functions
args = {
    pc - int
    ram - a list
    ACC - int
    IX - int
    zmp - bool - comparison flag: equal(True), not equal(False)
    hlt - bool - halt flag
    err - string - execution result - default: execution successful
}

[   , , , , , inc, 12, , , sto, ,jmp ]

def stubFunc(args):
    -update pc
    (in ldd case pc+= 2)
    -do stuff
    (in ldd case:)
    registers["EE"] = ram[int(ram[pc+1], 16)]
"""

def LDM(args):
    args[ACC] = args[ram][args[pc]+1]
    args[pc] += 2

def LDD(args):
    addrss = args[ram][args[pc]+1]
    args[ACC] = args[ram][addrss]
    args[pc] += 2

def LDI(args):
    addrss = args[ram][args[pc]+1]
    value = args[ram][addrss]
    args[ACC] = value
    args[pc] += 2

def LDX(args):
    addrss = args[ram][args[pc]+1]
    newAddrss = addrss + args[IX]
    args[ACC] = args[ram][newAddrss]
    args[pc] += 2

def LDR(args):
    args[IX] = args[ram][args[pc]+1]
    args[pc] += 2

def STO(args):
    args[ram][args[pc]+1] = args[ACC]
    args[pc] += 2

def ADD(args):
    args[ACC] += args[ram][args[pc]+1]
    args[pc] += 2

def INC(args):
    if args[ram][args[pc]+1] == "EE":
        args[ACC] += 1
    elif args[ram][args[pc]+1] == "FF":
        args[IX] += 1
    else:
        args[hlt] = True
        args[err] = "Register error: operand is not ACC or IX."
    args[pc] += 2

def DEC(args):
    if args[ram][args[pc]+1] == "EE":
        args[ACC] -= 1
    elif args[ram][args[pc]+1] == "FF":
        args[IX] -= 1
    else:
        args[hlt] = True
        args[err] = "Register error: only ACC and IX can be decremented."
    args[pc] += 2

def JMP(args):
    args[pc] = args[ram][args[pc]+1]

def CMP(args):  #format: CMP ADDRESSINGMODE OPERAND
    args[zmp] = True
    if args[ram][args[pc]+1] == 0:  #immediate addressing mode
        num = args[ram][args[pc]+2]
        if num == args[ACC]:
            args[zmp] = True
        else:
            args[zmp] = False

    elif args[ram][args[pc]+1] == 1:   #direct addressing mode
        addrss = args[ram][args[pc]+2]
        if args[ram][addrss] == args[ACC]:
            args[zmp] = True
        else:
            args[zmp] = False
    else:   #neither immediate nor direct addressing modes
        args[hlt] = True
        args[err] = "Addressing mode error: only immediate or direct addressing modes are allowed"
    args[pc] += 3

def JPE(args):
    addrss = args[ram][args[pc]+1]
    if args[zmp] == True:   #they are equal
        args[pc] = addrss
    else:   #they are not equal, continue the execution without jumping
        args[pc] += 2

def JPN(args):
    addrss = args[ram][args[pc]+1]
    if args[zmp] == False:  #they are not equal
        args[pc] = addrss
    else:   #they are equal, continue the execution without jumping
        args[pc] += 2

def inStub(chrcter):
    return chrcter

def IN(args):
    chrcter = inStub(chrcter)
    args[ACC] = ord(chrcter)
    args[pc] += 1

def outStub(chrcter):
    pass

def OUT(args):
    chrcter = chr(args[ACC])
    outStub(chrcter)
    args[pc] += 1

def END(args):
    print(args[ACC])
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
