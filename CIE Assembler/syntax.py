OPCODETOHEX = { #CONSTANT Dictionary to hold opcodes to their respective hexcodes
    "LDM":"0A",
    "LDD":"0B",
    "LDI":"0C",
    "LDX":"0D",
    "LDR":"0E",
    "STO":"0F",
    "ADD":"1A",
    "INC":"1B",
    "DEC":"1C",
    "JMP":"1D",
    "CMP":"1E",
    "JPE":"1F",
    "JPN":"2A",
    "IN":"2B",
    "OUT":"2C",
    "END":"2D"
}

HEXTOFUNCTION = { #CONSTANT Dictionary to hold hexcodes to the functions we will call
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
