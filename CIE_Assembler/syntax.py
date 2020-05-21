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

'''
HEXTOFUNCTIONDICT = {
    "0A":LDM,
    "0B":LDD,
    "0C":LDI,
    "0D":LDX,
    "0E":LDR,
    "0F":STO,
    "1A":ADD,
    "1B":INC,
    "1C":DEC,
    "1D":JMP,
    "1E":CMP,
    "1F":JPE,
    "2A":JPN,
    "2B":IN,
    "2C":OUT,
    "2D":END
}

def LDD(args):

    make it do stuff


ram = [ , , ,ldd ,100 , , , , , , , , ]
             ^
             pc


!!!
EVERYTHING IN RAM IS IN HEX


!!!
a = []
b = a
registers = {"acc": }
HSDJGF[<0A>](pc,ram,registers)

interpreter:
    looks at ram[pc]
    and calls the method

# dictionary that is passed to all functions
args = {
    pc - int
    ram - a list
    ACC - int
    IX - int
    ZMP - bool - comparison flag
    HLT - bool - halt flag
    err - string - execution result - default: execution successful
    


}


[   , , , , , inc, 12, , , sto, ,jmp ]
def INC(args):

    ram[pc+1] == "EE"
        args[ACC] += 1
    ram[pc+1] == "FF"

    else
        args[HLT] = True


def stubFunc():
    -update pc
    (in ldd case pc+= 2)
    -do stuff
    (in ldd case:)
    registers["EE"] = ram[int(ram[pc+1], 16)]


'''
