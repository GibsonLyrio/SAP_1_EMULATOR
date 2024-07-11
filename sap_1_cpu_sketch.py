# ==============================================================
# This versions is a sketch, it's dosent work properly, I decide
# to maintain this because can give some insides of my old codes 
# ==============================================================
# project of an CPU emulator based on SAP 1 (Simple as Possible)
# variables writed in "snake_case" and functions in "PascalCase"
# ==============================================================
# typer lib for console
# tabulate lib for tables in console
# pygame for iteractible window
# ==============================================================

print(f'\033[32m')

# importações:
from time import sleep, perf_counter
import pygame # type: ignore
# ----

# definições gerais:
byte = 0x00
word = 0x0000

    # define control bits, 36 bits width
END       = 0b00000000000000000000000000000000000
HLT       = 0b00000000000000000000000000000000000    # helt the clock
AI        = 0b00000000000000000000000000000000000    # accumulator register in
AO        = 0b00000000000000000000000000000000000    # accumulator register out
ES        = 0b00000000000000000000000000000000000    # ALU subtraction enable
EO        = 0b00000000000000000000000000000000000    # ALU output enable
TI        = 0b00000000000000000000000000000000000    # temporary register in
TO        = 0b00000000000000000000000000000000000    # temporary register out
BI        = 0b00000000000000000000000000000000000    # B register in
BO        = 0b00000000000000000000000000000000000    # B register out
CI        = 0b00000000000000000000000000000000000    # C register in
CO        = 0b00000000000000000000000000000000000    # C register out
RI        = 0b00000000000000000000000000000000000    # RAM in
RO        = 0b00000000000000000000000000000000000    # RAM out
MRI       = 0b00000000000000000000000000000000000    # memory address register in
IRI       = 0b00000000000000000000000000000000000    # instruction register in

A_LOAD    = 32
A_EN      = 31
A_INC     = 30
A_DEC     = 29
B_LOAD    = 28
B_EN      = 27
B_INC     = 26
B_DEC     = 25
C_LOAD    = 24
C_EN      = 23
C_INC     = 22
C_DEC     = 21
FLAGS_LDA = 20
FLAGS_LDB = 19
FLAGS_LDC = 18
ALU_OP2   = 17
ALU_OP1   = 16
ALU_OP0   = 15
ALU_LD    = 14
ALU_EN    = 13
IR_LOAD   = 12
PC_INC    = 11
PC_LOAD   = 10
PC_EN     = 9
MAR_LOADH = 8
MAR_LOADL = 7
MDR_LOAD  = 6
MDR_EN    = 5
RAM_LOAD  = 4
RAM_ENH   = 3
RAM_ENL   = 2
CALL      = 1
RET       = 0
# ---

# definindo clock da simulação:

# ----

# definindo atributos gerais dos componentes:
class Component:
    def __init__(self):
        self.io_port = byte
        self.ctrl_port = byte
        self.bits_stored = byte

    def Reset(self):
        self.io_port = byte
        self.ctrl_port = byte
        self.bits_stored = byte

    def BeingLow(self):
        pass

    def RissingEdge(self):
        pass

    def BeingHigh(self):
        pass

    def FallingEdge(self):
        pass
# ----

# definindo as funções de um componente registrador:
class Reg(Component):

    def Store(self, new_value):
        self.bits_stored = new_value

    def BeingLow(self):
        pass

    def RissingEdge(self, ctrl_line):
        pass

    def BeingHigh(self):
        pass

    def FallingEdge(self):
        pass
# ---

# definindo a classe computer:
class Computer:
    def __init__(self):                         # create new instance:
        self.components = []                        # start instance without components;
        self.Reset()                                # set "bus_line", "simmulatio_time" and "last_ticks" appropriately;
        self.clock_rate = 2 * 1e+6                  # default: 2 MHz;

    def Reset(self):                            # reset values and clock of an instance of computer:
        for component in self.components:
            component.Reset()                       # for all current components, call Reset() of each component;
        self.simulation_time = 0.0                  # set simulation_time as 0;
        self.bus_line = byte                        # set bus_line as 0 with 8bits width;
        self.last_ticks = perf_counter()            # set las_ticks with current clock value of Host computer;

    def Update(self):
        self.now_ticks = perf_counter()
        elapsed_time = self.now_ticks - self.last_ticks
        self.simulation_time += elapsed_time
        self.last_ticks = self.now_ticks

        clock_period = 1 / self.clock_rate

        while (self.simulation_time > clock_period):
            self.simulation_time -= clock_period

    def DirectConnection(component: Component):
        pass
# ----

# testes:
def main():
    cpu = Computer()
pygame.init()
screen = pygame.display.set_mode((428, 240))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        print(event.type)
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    keys = pygame.get_pressed()

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

if __name__ == "__main__":
    main()
    
print(f'\033[m')
