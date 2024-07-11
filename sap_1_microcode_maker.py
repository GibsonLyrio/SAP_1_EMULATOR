'''
This is a controller file maker for the control unit of SAP (Simple As Possible) 1 CPU,
more information about this archtecture availible in "Digital Computer Electronics" by
Albert Paul Malvino;

Gibson Lyrio | June 7th 2024
'''

  # define control bits, 16 bits width:

blank = 0b0000000000000000      # blank word
hlt   = 0b0000000000000001      # helt the cpu
xx    = 0b0000000000000010      # undefined
yy    = 0b0000000000000100      # undefined
Oi    = 0b0000000000001000      # input Out register  (binary display)
Bi    = 0b0000000000010000      # input B register    (temporary)
Eo    = 0b0000000000100000      # output ALU value
Es    = 0b0000000001000000      # subtract ALU mode
Ao    = 0b0000000010000000      # output A register   (accumulator)
Ai    = 0b0000000100000000      # input A register    (accumulator)
IRo   = 0b0000001000000000      # output IR register  (4 least significant bits)
IRi   = 0b0000010000000000      # input IR register   (instruction register)
RMo   = 0b0000100000000000      # output RAM
MRi   = 0b0001000000000000      # input MAR register  (memory addresss register)
PCo   = 0b0010000000000000      # output PC register  (program counter)
PCi   = 0b0100000000000000      # input PC
PCe   = 0b1000000000000000      # increase PC
# ---

max_steps = 8                   # I use a 3 bits step counter inside control unit
microcode = []                  # start microcode in blank
memory = 16 * 8                 # SAP-1 has 4 bits for set an instruction (times 3 bits for step)

# define fatch cycle:
fatch_1 = PCo | MRi
fatch_2 = RMo  | IRi | PCe


# start memory slots:
for addrs in range(memory):
  microcode.append(blank)

def montar(code: list, addr):
  steps = len(code)

  if addr <= (memory - max_steps):
    if microcode[addr] == (blank):
      if steps <= max_steps - 2:
        restante = max_steps

        # add fetch cycle at beggin:
        microcode[addr] = fatch_1
        addr += 1               # increase address by 1;
        microcode[addr] = fatch_2
        addr += 1               # increase address by 1;
        restante -= 2

        # add the steps:
        for step in code:
          microcode[addr] = step
          addr += 1           # increase address by 1;
          restante -= 1

        # fill blank the remain steps:
        for step in range(restante):
          microcode[addr] = blank
          addr += 1           # increase address by 1;
      else:
        raise SyntaxError(f"\033[3;31mYou put ({steps}) steps\nPut until ({max_steps-2}) steps\033[m\n")
    else:
      print(f"{microcode[addr]}")
      raise SyntaxError(f"\033[3;31mThe last command try\nOverwrite the addrs 0b{addr:07b} to 0b{(addr + max_steps - 1):07b}\033[m\n")
  else:
    raise SyntaxError(f"\033[3;31mThe last command overflow the\nMemory, addr max for comands -> 0x{(memory - max_steps):07b}\033[m\n")


# define commands:
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

# ^^ if needed, add more commands here ^^ #

opcodes = [
  ["LDA", LDA_opcode],
  ["ADD", ADD_opcode],
  ["SUB", SUB_opcode],
  ["OUT", OUT_opcode],
  ["HLT", HLT_opcode],
]

# logic for visualization feature in console:
blocks = int(memory / max_steps)                  # each block has 8 steps;
index = 0

print("\n╭――――――――――――――――――╮")
print("│ controll diagram │")
print("╰――╥――――――╥――――――――╯")
print("╭――╨――――――╨――╮")
for block in range(blocks):
  if microcode[index] == blank:
    print(f"│ \033[30m{block:04b} (NOP)\033[m │")
    microcode[index + 0] = fatch_1
    microcode[index + 1] = fatch_2
  else:
    for i in opcodes:
      if i[1] == block:
        mnemonic = i[0]
        opcode = i[1]

    print(f"│ {opcode:04b} ({mnemonic}) │")
  index += 8
print(f"╰――――――――――――╯")
# ----

# creating the files:
with open("controller.txt", "w") as archive:      # create the txt file used by v1.0 and v1.1
  index = 1
  for x in microcode:
    archive.write(f"{format(x, "016b")}")
    if index < len(microcode):
      archive.write("\n")
    index += 1

with open("controller.bin", "wb") as archive:     # create the binary file used by v1.2
  for x in microcode:
    word = int(x).to_bytes(2)
    archive.write(word)
print(f"\n\033[7;32m Success! \033[m\n")
