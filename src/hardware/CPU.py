'''
CPU:
  Do the aritimetic and logic operation, attached in motherboard, directly
  connected to RAM.

  SAP_2
'''


# with open('ROM.bin', 'rb') as rom_file:
#   while True:
#     data = rom_file.read(5)  # Ler 5 bytes por ciclo
#     if not data:  # Se chegar ao final do arquivo
#         break
#     # Converte os 5 bytes em um número de 40 bits
#     control_word = int.from_bytes(data, byteorder='big')
#     print(f'Control Word: {control_word:040b}')  # Exibe o valor em binário

#-------------------------------------------------------------------------------
# GENERAL DEFINES AND IMPORTS
#-------------------------------------------------------------------------------

# import numpy to use "uint" type and bitwise operations beetwen them
import numpy

# some alias to numpy types
Byte = numpy.uint8      # 0xFF
Word = numpy.uint16     # 0xFFFF
Dword = numpy.uint32    # 0xFFFFFFFF
Qword = numpy.uint64    # 0xFFFFFFFFFFFFFFFF

# define 40 control bits to use in "Control Word" of micro instructions
sig_undefined = 0x0000000001
sig_end       = 0x0000000002
sig_hlt       = 0x0000000004
sig_a_load    = 0x0000000008
sig_a_en      = 0x0000000010
sig_a_inc     = 0x0000000020
sig_a_dec     = 0x0000000040
sig_b_load    = 0x0000000080
sig_b_en      = 0x0000000100
sig_b_inc     = 0x0000000200
sig_b_dec     = 0x0000000400
sig_c_load    = 0x0000000800
sig_c_en      = 0x0000001000
sig_c_inc     = 0x0000002000
sig_c_dec     = 0x0000004000
sig_flags_lda = 0x0000008000
sig_flags_ldb = 0x0000010000
sig_flags_ldc = 0x0000020000
sig_alu_op2   = 0x0000040000
sig_alu_op1   = 0x0000080000
sig_alu_op0   = 0x0000100000
sig_alu_ld    = 0x0000200000
sig_alu_en    = 0x0000400000
sig_ir_load   = 0x0000800000
sig_pc_inc    = 0x0001000000
sig_pc_load   = 0x0002000000
sig_pc_en     = 0x0004000000
sig_mar_loadh = 0x0008000000
sig_mar_loadl = 0x0010000000
sig_mdr_load  = 0x0020000000
sig_mdr_en    = 0x0040000000
sig_ram_load  = 0x0080000000
sig_ram_enh   = 0x0100000000
sig_ram_enl   = 0x0200000000
sig_call      = 0x0400000000
sig_ret       = 0x0800000000
sig_undefined = 0x1000000000
sig_undefined = 0x2000000000
sig_undefined = 0x4000000000
sig_undefined = 0x8000000000
#END----------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# DEFINE GENERAL COMPONENT CLASS
#-------------------------------------------------------------------------------

class Component:
  def __init__(self):
    pass
  
  def Reset(self):
    pass
  def BeingLow(self):
    pass
  def RisingEdge(self):
    pass
  def BeingHigh(self):
    pass
  def FallingEdge(self):
    pass

#END----------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# DEFINE ALL NEEDED BUS (CONTROL, ADDRESS, DATA)
#-------------------------------------------------------------------------------

