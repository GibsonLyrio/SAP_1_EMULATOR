### by Gibson Lyrio - June 7th 2024 ###
# this is a compiler of microcode for the control unit of SAP 1 archtecture
# more info availible in "Digital Computer Electronics" by Albert Paul Malvino

    # define control bits, 16 bits width
blank= 0b0000000000000000    # blank word
hlt  = 0b0000000000000001    # helt the cpu
xx   = 0b0000000000000010    # undefined
yx   = 0b0000000000000100    # undefined
Oi   = 0b0000000000001000    # input out register (binary display)
Bi   = 0b0000000000010000    # input b (tmp) register
Eo   = 0b0000000000100000    # output alu value
Es   = 0b0000000001000000    # subtract alu mode
Ao   = 0b0000000010000000    # output acc register
Ai   = 0b0000000100000000    # input acc register
IRo  = 0b0000001000000000    # output IR (less 4 bits)
IRi  = 0b0000010000000000    # input IR
RMo  = 0b0000100000000000    # chip enable RAM
MRi  = 0b0001000000000000    # input MAR
PCo  = 0b0010000000000000    # output PC
PCi  = 0b0100000000000000    # input PC
PCe  = 0b1000000000000000    # increase PC
# ---

max_steps = 8           # I use a 3 bits step counter inside control unit
microcode = []          # start microcode in blank
memory = 16 * 8         # SAP-1 has 4 bits for set an instruction (plus 3 bits for step)

# Definindo fatch cycle:
fatch_1 = PCo | MRi
fatch_2 = RMo  | IRi | PCe


# Inicia slots da memoria
for addrs in range(memory):
    microcode.append(blank)

def montar(code: list, addr):
    steps = len(code)

    if addr <= (memory - max_steps):
        if microcode[addr] == (blank):
            if steps <= max_steps - 2:
                restante = max_steps

                # Adciona fetch cycle no inicio:
                microcode[addr] = fatch_1
                addr += 1               # avança o endereço
                microcode[addr] = fatch_2
                addr += 1               # avança o endereço
                restante -= 2

                # Adiciona as etapas:
                for step in code:
                    microcode[addr] = step
                    addr += 1           # avança o endereço
                    restante -= 1

                # Preenche o restante vazio:
                for step in range(restante):
                    microcode[addr] = blank
                    addr += 1           # avança o endereço
            else:
                print(f"\n\033[3;31mERROR: Você colocou {steps} etapas\nColoque no máximo {max_steps-2}\033[m\n")
                raise TypeError()
        else:
            print(f"{microcode[addr]}")
            print(f"\n\033[3;31mERROR: O ultimo comando tenta\nsobrescrever os endereços de 0b{addr:08b} ~ 0b{(addr + max_steps):08b}\033[m\n")
            raise TypeError()
    else:
        print(f"\n\033[3;31mERROR: O ultimo comando estourou a\nmemória, addr max para comando -> 0x{(memory - max_steps):08b}\033[m\n")
        raise TypeError()


# Definindo comandos:
LDA = [
    (MRi | IRo),
    (RMo | Ai ),
]
LDA_opcode = 0b0000
montar(LDA, LDA_opcode << 3)

ADD = [
    (MRi | IRo),
    (RMo | Bi ),
    (Eo  | Ai ),
]
ADD_opcode = 0b0001
montar(ADD, ADD_opcode << 3)

SUB = [
    (MRi | IRo),
    (RMo | Bi ),
    (Es  | Eo  | Ai ),
]
SUB_opcode = 0b0010
montar(SUB, SUB_opcode << 3)

OUT = [
    (Ao  | Oi ),
]
OUT_opcode = 0b1110
montar(OUT, OUT_opcode << 3)

HLT = [
    (hlt)
]
HLT_opcode = 0b1111
montar(HLT, HLT_opcode << 3)

# ^^ Adcione novos comando a partir daqui ^^ #

opcodes = [
    ["LDA", LDA_opcode],
    ["ADD", ADD_opcode],
    ["SUB", SUB_opcode],
    ["OUT", OUT_opcode],
    ["HLT", HLT_opcode],
]

# aplicar NOP para os blocos vazios:
blocos = int(memory / max_steps)             # cada bloco possui 8 steps;
index = 0


print("\n╭――――――――――――――――――╮")
print("│ controll diagram │")
print("╰――╥――――――╥――――――――╯")
print("╭――╨――――――╨――╮")
for bloco in range(blocos):
    if microcode[index] == blank:
        print(f"│ \033[30m{bloco:04b} (NOP)\033[m │")
        microcode[index + 0] = fatch_1
        microcode[index + 1] = fatch_2
    else:
        for i in opcodes:
            if i[1] == bloco:
                mnemonic = i[0]
                opcode = i[1]

        print(f"│ {opcode:04b} ({mnemonic}) │")
    index += 8
print(f"╰――――――――――――╯")
# ----

with open("controller.txt", "w") as archive:
    index = 1
    for x in microcode:
        archive.write(f"{format(x, "016b")}")
        if index < len(microcode):
            archive.write("\n")
        index += 1

with open("controller.bin", "wb") as archive:
    for x in microcode:
        word = int(x).to_bytes(2)
        archive.write(word)
print(f"\n\033[7;32m Success! \033[m\n")
