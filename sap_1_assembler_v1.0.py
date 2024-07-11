"""
Assembler to machine code of CPU SAP_1, compatible with all v1.x;
When you run this code, automatcaly generete the OPCODE TABLE and
the file for control unit read;
This assembler don't has a fancy errors detection, so pay attention
in your assembly code;

Assembly code exemple:
assembly = '''
:$00                        # set the address of next command;
LDA $f                      # the "$" means that value is a address;
ADD $e
ADD $d
SUB $c
OUT #0                      # the "#" means that value is a literally value;

:$0c                        # don't forget to add ":" to tell this is a starter, and "$" to tell the address;
#20                         # at the start of line, the "#" also means that it's a value;
#18
#14
#10
'''

Yes you can add how many blank spaces and breake lines what you want
the code will work fine, because the tokenization process remove all
blank spaces between the opcode and operand, so "LDA     $" is read
"LDA$f" this is why use "$" necesarrily to split command of value,
and the line of command are splited by the "\n" and after split all
blank line are removed, so the lines "OUT #0 \n \n :$0c" are read
as ("OUT#0", "", ":$0c" ) and the blank at the mid are removed.

Gibson Lyrio | June 5th 2024
"""

from sap_1_microcode_maker import opcodes     # this import and run the opcodes for sap 1 controller unit;

def Assembler(assembly: str):
    assembly = assembly.upper()
    assembly = assembly.replace(" ", "")
    assembly = assembly.split("\n")
    starter_addrs = 0
    memory_size = 16                    # SAP_1 has 16 memorry address;
    memory_width = 8                    # SAP_1 has 8 bit in wich memory address;
    source_code = []
    current_line = -1

    for addr in range(memory_size):
        source_code.append(0xf0)        # initialize memory with HLT comand in all adderess;

    print("╭――――――――――――――――╮")
    print("│ CODE ASSEMBLED │")
    print("╰――╥――――――――――╥――╯")
    print("╭――╨――――――――――╨――――――――――――――╮")
    
    for mnemonic in assembly:           # for wich line in assembly: 
        current_line += 1               # increase pointer to current line, only for error localization;
        if mnemonic != "":                                          # exclude blank lines;
            has_starter = mnemonic.find(":")                        # verify if is has starter addresss;
            has_addrs = mnemonic.find("$")                          # verify if is has a address value;
            has_value = mnemonic.find("#")                          # verify if is a imediataly value;

            if has_starter == 0:                                    # if the ":" is in first char; (blank spaces ignored)
                if has_addrs == 1:                                  # if "$" is in second char; (blank spaces ignored)
                    starter_addrs = int(mnemonic[2:], base=16)      # set appropely the starter address;
                    
            elif has_starter < 0:         # if not is a starter, then:
                if has_addrs > 0:                                   # if has address do this:
                    txt_opcode = mnemonic.split("$")[0]
                    txt_operand = mnemonic.split("$")[1]
                    for value in opcodes:
                        if value[0] == txt_opcode:
                            opcode = value[1] << 4                      # set appropely the code;
                    operand = int(txt_operand, base=16) & 0x0f          # set appropely operand;
                    source_code[starter_addrs] = (opcode | operand)     # insert opcode and operand in target address;
                    starter_addrs += 1                                  # increment the address for next line assembly;

                elif has_value == 0:
                    value = mnemonic.split("#")
                    source_code[starter_addrs] = int(value[1], base=16)
                    starter_addrs += 1

                elif has_value > 0:                                 # else if has value do this:            
                    txt_opcode = mnemonic.split("#")[0]
                    txt_operand = mnemonic.split("#")[1]
                    opcode_finded = False
                    for value in opcodes:
                        if value[0] == txt_opcode:
                            opcode = value[1] << 4                      # set appropely the code;
                            opcode_finded = True                        # sinalize that opcode was finded;
                    if opcode_finded == False:
                        print(f"\033[31m\nERROR: ({txt_opcode}) isn't a valid command.")
                        print(f"line: {current_line}, '{assembly[current_line]}'\033[m\n")
                        raise TypeError
                    operand = int(txt_operand, base=16) & 0x0f          # set appropely operand;
                    source_code[starter_addrs] = (opcode | operand)     # insert opcode and operand in target address;
                    starter_addrs += 1                                  # increment the address for next line assembly;

                else:
                    print(f"\033[31m\nERROR: command ({mnemonic}) are missing some argument.")
                    print(f"line: {current_line}, '{assembly[current_line]}'\033[m\n")
                    raise TypeError

    for i in source_code:
        for value in opcodes:
            if value[1] == (i >> 4): i_opcode = value[0]
        y = "\033[33m"
        b = "\033[34m"
        d = "\033[m"
        print(f"│ {y}{(i >> 4):04b}{b}{(i & 0x0f):04b}{d} = {y}{i_opcode} {b}({(i & 0x0f):01x}){d} or {b}0x{i:02x}{d} │")
    print(f"╰――――――――――――――――――――――――――――╯")

    return source_code

assembly = '''
:$00
LDA $f
ADD $e
SUB $d
OUT #0

:$d
#4
#3
#5
'''

source_code = Assembler(assembly)

with open("ROM.txt", "w") as archive:
    index = 0
    for i in source_code:
        archive.write(f"{i:08b}")
        index += 1
        if index < len(source_code): archive.write("\n")
with open("ROM.bin", "wb") as archive:
    for i in source_code:
        i_byte = int(i).to_bytes(1)
        archive.write(i_byte)
