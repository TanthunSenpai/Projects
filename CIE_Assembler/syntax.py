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
"RAM" = [ , , ,ldd ,160 , , , , , , , , ]
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
    "PC" - hex str
    "RAM" - a list of hex str
    "ACC" - hex str
    "IX" - hex str
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

def denHex(x):
    # Converts a denary integer into a formatted hexadecimal string
    l =  hex(x)[2:].upper()
    if len(l) == 1:
        l = "0" + l
    return l

def LDM(args):
    args["ACC"] = denHex(int(args["RAM"][(int(args["PC"],16)+1)%256],16)%256)  #in hex string
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def LDD(args):
    addrss = int(args["RAM"][(int(args["PC"],16)+1)%256],16)   #in denary
    args["ACC"] = denHex(int(args["RAM"][addrss],16)%256)  #in hex string
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def LDI(args):
    addrss = int(args["RAM"][(int(args["PC"],16)+1)%256],16)   #in denary
    value = int(args["RAM"][addrss],16)         #in denary, the second address
    args["ACC"] = value     #in hex string
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def LDX(args):
    addrss = int((args["RAM"][(int(args["PC"],16)+1)%256]),16)  #in denary
    newAddrss = (addrss + int(str(args["IX"]),16)) % 256    #in denary
    args["ACC"] = denHex(int(args["RAM"][newAddrss],16))   #in hex string
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex strting

def LDR(args):
    args["IX"] = denHex(int(args["RAM"][(int(args["PC"],16)+1)%256],16))   #in hex string
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def STO(args):
    addrss = int(args["RAM"][(int(args["PC"],16)+1)%256], 16)   #in denary, pointer
    args["RAM"][addrss] = denHex(int(args["ACC"],16))   #in hex string
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def ADD(args):
    value = int(args["RAM"][(int(args["PC"],16)+1)%256],16)     #in denary
    args["ACC"] = denHex((int(args["ACC"], 16) + value) % 256) #in hex denary
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def INC(args):
    if args["RAM"][(int(args["PC"],16)+1)%256] == "EE":
        args["ACC"] = denHex((int(args["ACC"],16)+1)%256)  #in hex string
    elif args["RAM"][(int(args["PC"],16)+1)%256] == "FF":
        args["IX"] = denHex((int(args["IX"],16)+1)%256)    #in hex string
    else:
        args["halt"] = True
        args["errorMsg"] = "Register error: register is not one of ACC or IX."
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def DEC(args):
    if args["RAM"][(int(args["PC"],16)+1)%256] == "EE":
        args["ACC"] = denHex((int(args["ACC"],16)-1)%256)  #in hex string
    elif args["RAM"][(int(args["PC"],16)+1)%256] == "FF":
        args["IX"] = denHex((int(args["IX"],16)-1)%256)    #in hex string
    else:
        args["halt"] = True
        args["errorMsg"] = "Register error: register is not one of ACC or IX."
    args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def JMP(args):
    addrss = int(args["RAM"][(int(args["PC"],16)+1)%256],16)   #format hex address to hex string
    args["PC"] = denHex(addrss)



def CMP(args):  #format: CMP ADDRESSINGMODE OPERAND
    if int(args["RAM"][(int(args["PC"],16)+1)%256],16) == 1:  #immediate addressing mode
        num = int(args["RAM"][(int(args["PC"],16)+2)%256],16)   #in denary
        if num == int(args["ACC"],16):     #both in denary for comparison
            args["ZMP"] = True
        else:
            args["ZMP"] = False

    elif int(args["RAM"][(int(args["PC"],16)+1)%256],16) == 0:   #direct addressing mode
        addrss = int(args["RAM"][int(args["PC"],16)+2],16)  #in denary, pointer
        if int(args["RAM"][addrss],16) == int(args["ACC"],16): #both numbers are in denary for comparison
            args["ZMP"] = True
        else:
            args["ZMP"] = False
    else:   #neither immediate nor direct addressing modes
        args["halt"] = True
        args["errorMsg"] = "Addressing mode error: only immediate or direct addressing modes are allowed"
    args["PC"] = denHex((int(args["PC"],16) + 3) % 256)    #in hex string

def JPE(args):
    addrss = int(args["RAM"][(int(args["PC"],16)+1)%256],16)    #in denary
    if args["ZMP"] == True:   #case: equal
        args["PC"] = addrss #in denary, PC is a pointer
    else:   #case: not equal, continue.
        args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def JPN(args):
    addrss = int(args["RAM"][(int(args["PC"],16)+1)%256],16)    #in denary
    if args["ZMP"] == False:  #case: not equal
        args["PC"] = addrss     #in denary, PC is a pointer
    else:   #case: equal, continue.
        args["PC"] = denHex((int(args["PC"],16) + 2) % 256)    #in hex string

def inStub(letter):
    return letter

def IN(args):
    inStub(args)
    args["inFlag"] = True
    args["PC"] = denHex((int(args["PC"],16) + 1) % 256)    #in hex string

def outStub(chrcter):
    pass

def OUT(args):
    chrcter = chr(int(args["ACC"],16)) #convert hex number to denary to ASCII
    outStub(chrcter)
    args["PC"] = denHex((int(args["PC"],16) + 1) % 256)    #in hex string

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

if __name__ == "__main__":

    args = {
        "PC": "00",
        "RAM": ["00","02","03","0F","0B","00","00","00","00","00","00","00","00","00","00","00"],
        "ACC": "FF",
        "IX": "01",
        "ZMP": False,
        "halt": False,
        "errorMsg": ""
    }


    #LDM(args)
    #LDD(args)
    #LDI(args)
    #LDX(args)
    #LDR(args)
    #STO(args)
    #ADD(args)
    #INC(args)
    #DEC(args)
    #JMP(args)
    #CMP(args)
    #JPE(args)
    #JPN(args)

    #IN and OUT funcs left for testing


    print("PC", args["PC"])
    print("ACC", args["ACC"])
    print("ACC type", type(args["ACC"]))
    print("IX", args["IX"])
    print("IX type", type(args["IX"]))
    print(args["RAM"])
    print("MSG", args["errorMsg"])
    print("ZMP", args["ZMP"])
