"""
Project of an CPU emulator based on SAP_1 (Simple as Possible),
you can find more info about this archtecture in "digital computer
electronics" by albert paul malvino;

Variables writed in "snake_case", and functions in "PascalCase";

In some future moment this project will be remaked in C++ for
better performance, and availible in my GitHub page;

v1.1 has a easy visualization of components, RAM, and display
comparally with v1.0, in general is the same, only visual changes

Gibson Lyrio | June 4th 2024 
"""

# general defines:
byte = 0x00
word = 0x0000

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


# define bus line:
class BusLine:
    def __init__(self):
        self.stored = byte

    def Get(self):
        return self.stored

    def Put(self, value: int):
        self.stored = value
# ----


# define control line:
class CtrlLine:
    def __init__(self):
        self.stored = word

    def Get(self):
        return self.stored

    def Put(self, value: int):
        if value >= 0x0000 and value <= 0xffff:
            self.stored = value
        else:
            print(f"ERROR: valor {hex(value)} é inválido, ctrl_line aceita entre 0x0000 e 0xffff")
# ----


# define general attributes of a component:
class Component:
    def __init__(self):
        pass

    def Reset(self):
        pass
    def BeingLow(self):
        pass
    def RissingEdge(self):
        pass
    def BeingHigh(self):
        pass
    def FallingEdge(self):
        pass
# ----


# define register:
class Register(Component):
    def __init__(
            self,                                   # create a new instance:
            bus_line: BusLine,
            ctrl_line: CtrlLine,
            in_mask: int,
            out_mask: int,
            count_mask: int,
            out_lsb: int,
            name: str,
    ):
        self.name = name                                # only debug feature;
        self.byte_stored = byte                         # start with a clear byte (0x00);
        self.bus_line = bus_line                        # pointer to bus line;
        self.ctr_line = ctrl_line                       # pointer to control line;
        self.in_mask = in_mask                          # mask for control signal input;
        self.out_mask = out_mask                        # mask for control signal output;
        self.count_mask = count_mask                    # mask for control signal count (increase current value);
        self.out_lsb = out_lsb                          # output only 4 Least Significant Bits (used by IR);

    # all functions:
    def Store(self):                                # store the value from bus:
        self.byte_stored = self.bus_line.Get()
    
    def Increment(self):                            # increase the current value stored:
        self.byte_stored += 1

    def Output(self):                               # output stored value to bus:
        if self.out_lsb == 0x0f:
            self.bus_line.Put(self.byte_stored & 0x0f)
        else:
            self.bus_line.Put(self.byte_stored)

    def Get(self):                                  # return the value stored (used assyncronaly by ALU):
        return self.byte_stored
    
    def GetMSB(self):                               # return the Most Significant bits (used by IR to Controller):
        return int(self.byte_stored >> 4)
        
    def Reset(self):                                # reset stored value to 0:
        print(f"{self.name} Reset.")
    # ----

    # behavior by clock:
    def BeingLow(self):                             # behavior durring the low clock phase:
        if self.ctr_line.Get() & self.out_mask:
            self.Output()
            print(f"{self.name} -> Outputting to bus: 0x{self.byte_stored:02x}")

    def RissingEdge(self):                          # behavior durring the rissing edge clock:
        if self.ctr_line.Get() & self.in_mask:
            self.Store()
            print(f"{self.name} <- New value: 0x{self.byte_stored:02x}")


        elif (self.ctr_line.Get() & self.count_mask) or (self.count_mask == 0xff):
            self.Increment()
            print(f"{self.name} Increase to: 0x{self.byte_stored:02x}")
    # ----
# ---


# define ALU:
class ALU(Component):
    def __init__(                               # create a new instance:
            self,
            bus_line: BusLine,
            ctrl_line: CtrlLine,
            out_mask: int,
            sub_mask: int,
            reg_a: Register,
            reg_b: Register,
            name: str,
    ):
        self.name = name                            # only debug feature;
        self.byte_stored = byte                     # start with a clear byte (0x00);
        self.bus_line = bus_line                    # pointer to bus line;
        self.ctrl_line = ctrl_line                  # pointer to control line;
        self.out_mask = out_mask                    # mask for control signal input;
        self.sub_mask = sub_mask                    # mask for control signal subtract;
        self.reg_a = reg_a                          # pointer to register A;
        self.reg_b = reg_b                          # pointer to register B;

    # all functions:
    def Sum(self):                                  # store A + B;
        a_value = self.reg_a.Get()
        b_value = self.reg_b.Get()
        result = a_value + b_value
        if result == 0x00:
            self.byte_stored = 0x00
            # add here set zero flag logic
        elif result > 0xff:
            # add here unset flag logic
            self.byte_stored = result - 0xff
        elif result <= 0xff:
            # add here set carry flag logic
            self.byte_stored = result

    def Sub(self):                                  # store A - B;
        a_value = self.reg_a.Get()
        b_value = self.reg_b.Get()
        self.byte_stored = a_value - b_value
        if self.byte_stored < 0x00:
            pass

    def Calcule(self):
        if self.ctrl_line.Get() & self.sub_mask:
            self.Sub()
        else:
            self.Sum()

    def Output(self):                               # output stored value to bus:
        self.bus_line.Put(self.byte_stored)
    # ----

    # behavior by clock:
    def BeingLow(self):                             # behavior durring the low phase of clock:
        self.Calcule()
        if self.ctrl_line.Get() & self.out_mask:
            self.Output()
            print(f"{self.name} -> Outputting to bus: 0x{self.byte_stored:02x}")

    def BeingHigh(self):                            # behavior durring the high phase of clock:
        self.Calcule()
    # ----
# ----


# define controler:
class Controller(Component):
    def __init__(
            self,
            ctrl_line: CtrlLine,
            ir: Register,
            name: str,
            ):
        self.now_control_word = 0
        self.step_counter = 0b0
        self.microcode = []
        self.ctrl_line = ctrl_line
        self.ir = ir
        self.name = name

        with open("controller.txt", "r") as archive:
            control_txt = archive.read()
        control_splited = control_txt.split("\n")

        for control_word in control_splited:
            self.microcode.append(control_word)

    def SetControlWord(self):
        self.now_control_word = self.microcode[(self.ir.GetMSB() << 3) + self.step_counter]

    def FallingEdge(self):
        self.SetControlWord()
        self.ctrl_line.Put(int(self.now_control_word, 2))
        print(f"{self.name} <- Opcode ({self.ir.GetMSB():04b}) step ({self.step_counter:03b})")
        print(f"{self.name} -> {self.now_control_word}")
        self.step_counter += 1
        if self.step_counter >= 8: self.step_counter = 0b0
# ----

# # use this code to visualize what controller read from ROM.txt:
# 
# bus_line_test = BusLine()
# ctrl_line_test = CtrlLine()
# ir_test = Register(bus_line_test, ctrl_line_test, 0, 0, 0, 0, "")
# controller_test = Controller(ctrl_line_test, ir_test, "test")
# index = 0
# for control_word in controller_test.microcode:
#     if index % 8 == 0:
#         print("========")
#     print(f"\033[34m{(index >> 3):04b}\033[33m{(index & 0b0000111):03b}\033[m: {controller_test.microcode[index]}")
#     index += 1
# # ----


# define RAM:
class RAM(Component):
    def __init__(
            self,
            ctrl_line: CtrlLine,
            bus_line: BusLine,
            out_mask: int,
            mar: Register,
            name: str,
            ):
        self.stored = []
        self.current_value = byte
        self.ctrl_line = ctrl_line
        self.bus_line = bus_line
        self.out_mask = out_mask
        self.mar = mar
        self.name = name

        with open("ROM.txt", "r") as archive:
            rom_txt = archive.read()
        rom_splited = rom_txt.split("\n")

        for command in rom_splited:
            self.stored.append(int(command, 2))

    # all functions:
    def Output(self):                               # output current value to bus:
        self.current_value = self.stored[(self.mar.Get() & 0x0f)]
        self.bus_line.Put(self.current_value)
    # ----

    # behavior by clock:
    def BeingLow(self):                             # behavior durring the low clock phase:
        if self.ctrl_line.Get() & self.out_mask:
            self.Output()
            print(f"{self.name} -> Outputting to bus: 0x{self.current_value:02x}")
    # ----
# ----

## use this code to visualize what controller read from ROM.txt:
#
# bus_line_test = BusLine()
# ctrl_line_test = CtrlLine()
# mar_test = Register(bus_line_test, ctrl_line_test, 0, 0, 0, 0, "")
# ram = RAM(ctrl_line_test, bus_line_test, mar_test, "test")


# define binary display:
class Display(Component):
    def __init__(self, out_reg: Register):
        self.out_reg = out_reg

    def ShowDisplay(self):
        print(f"\n╭―――――――――――――――――――――――――╮")
        print(f"│ DISPLAY BIN  │ {self.out_reg.Get():08b} │")
        print(f"╰――╥―――――――――――╥――――――――――╯")
        print(f"╭――╨―――――――――――╨――――╮")
        print(f"│ DISPLAY HEX  │ {self.out_reg.Get():02x} │")
        print(f"╰―――――――――――――――――――╯\n")
# 

# define computer:
class Computer:
    def __init__(self):                             # create new instance:
        self.components = []                            # start instance without components;
        self.clock = 0                                  # this is for visualize in terminal, dont change notthing
        self.Reset()

    def Reset(self):                                # call reset function for all components in computer:
        for component in self.components: component.Reset()
        self.clock = 0

    def Update(self):                               # update function is a simulation of clock cycles:
        print(f"\n========== clock cycle {self.clock:03} ==========\033[32m")
        for component in self.components:               # the function needs this for loops SEPPARATELY 
            component.BeingLow()                        # because if was together, then de 1° item will
        for component in self.components:               # pass trouth the all clock cycle and after this
            component.RissingEdge()                     # the 2° will pass all clock cyle alone, etc...
        for component in self.components:               # ---
            component.BeingHigh()                       # so, putting loops like that, all items will
        for component in self.components:               # pass trouth the SAME clock phase toghether, all
            component.FallingEdge()                     # items BeingLow, after Rissing edge, after etc...
        print("\033[m============== Finished ==============\n")
        self.clock += 1

    def GetPointer(self, component: Component):     # return the pointer of a component that you insert:
        return (self.components[self.components.index(component)])
# ----


# tests:
def main():
    # starting instances:
    cpu = Computer()
    bus_line = BusLine()
    ctrl_line = CtrlLine()

    pc = Register(bus_line, ctrl_line, PCi, PCo, PCe, 0, "PC")
    reg_acc = Register(bus_line, ctrl_line, Ai, Ao, 0, 0, "Reg_A")
    reg_tmp = Register(bus_line, ctrl_line, Bi, 0, 0, 0, "Reg_B")
    reg_out = Register(bus_line, ctrl_line, Oi, 0, 0, 0, "Reg_Out")
    reg_mar = Register(bus_line, ctrl_line, MRi, 0, 0, 0, "MAR")
    reg_irg = Register(bus_line, ctrl_line, IRi, IRo, 0, 0x0f, "IR")
    alu = ALU(bus_line, ctrl_line, Eo, Es, reg_acc, reg_tmp, "ALU")
    controller = Controller(ctrl_line, reg_irg, "Controller")
    ram = RAM(ctrl_line, bus_line, RMo, reg_mar, "RAM")
    display = Display(reg_out)

    # pushing the instances in de cpu
    cpu.components.extend([
        pc,
        reg_acc,
        reg_tmp,
        reg_out,
        reg_mar,
        reg_irg,
        alu,
        controller,
        ram
        ])  # display dont need be inserted in the cpu, because it dont have bahavior by clock

    # main loop:
    while True:
        if ctrl_line.Get() == 1:                    # stop when HLT is active;
            break

        cpu.Update()                                # call the clock cycle for all componnets
        display.ShowDisplay()

    print("╭―――――――――――――╮")
    print("│ RAM content │")
    print("╰――╥―――――――╥――╯")
    index = 0
    print("╭――╨―――――――╨―――――╮")
    print("│ addr: \033[33mcode\033[34moprd\033[m │")
    print("│                │")
    for value in ram.stored:                        # this shows the content inside the RAM
        print(f"│ {index:04b}: \033[33m{(value>>4):04b}\033[34m{(value & 0x0f):04b}\033[m │")
        index += 1
    print("╰――――――――――――――――╯\n")

    # black = "\033[40m  \033[m"
    # white = "\033[47m  \033[m"
    # b = black
    # w = white

    # image_1 = [
    #     [w,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,w,],
    #     [b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,],
    #     [b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,],
    #     [b,b,b,b,b,b,b,b,b,w,b,b,b,b,b,b,b,b,b,],
    #     [b,b,b,b,b,b,b,b,w,b,w,b,b,b,b,b,b,b,b,],
    #     [b,b,b,b,b,b,b,b,b,w,b,b,b,b,b,b,b,b,b,],
    #     [b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,],
    #     [b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,],
    #     [w,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,w,],
    # ]

    # image_3 = [
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # ]

    # def DecoderByteToImg(Byte: list):
    #     image_decoded = []
    #     for value in Byte:
    #         index = 0
    #         temp = []
    #         value = f"{value:08b}"
    #         value = value.replace("0", b)
    #         value = value.replace("1", w)
    #         for bit in range(len(value)):
    #             temp.append(value[index])
    #             index += 1
    #         image_decoded.append(temp)
    #     return image_decoded

    # def Render(image: list):
    #     for y_line in image:
    #         for pixel in y_line:
    #             print(pixel, end="")
    #         print("\n", end="")
    #     print("")
    
    # Render(image_1)
    # Render(DecoderByteToImg(ram.stored))
# ----

if __name__ == "__main__":
    main()
