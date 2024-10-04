import os
# import pygame as pg
# import numpy as np
# from src.hardware.monitor import monitor_process
# from src.hardware.keyboard import keyboard_process
# from multiprocessing import Process, Queue


# def main():
#   # motherboard connections of all componnents
#   '''-------------------------------------------------'''
#   in_keyboard = Queue()       # keyboard <-
#   out_keyboard = Queue()      # keyboard -> monitor
#   '''-------------------------------------------------'''
#   in_monitor = out_keyboard   # monitor <- keyboard
#   out_monitor = None          # monitor ->
#   '''-------------------------------------------------'''

#   # Criando processos
#   keyboard = Process(target=keyboard_process, args=(in_keyboard, out_keyboard))
#   monitor = Process(target=monitor_process, args=(in_monitor,))

#   # Iniciando processos
#   keyboard.start()
#   monitor.start()

#   # Espera os processos terminarem (opcional)
#   keyboard.join()
#   monitor.join()

def main():
  os.system('cls' if os.name == 'nt' else 'clear')    # just clear screen
  while True:
    print("========================================")
    print("WELCOME TO SAP_2 EMULATOR")
    print("========================================")
    print("MAIN MENU")
    print("  [1] open assembler.py menu")
    print("  [2] open microcode-maker.py menu")
    print("  [3] boot the computer")
    user_choice = input("Chose one option (123): ")

    # open assembler menu
    if user_choice == 1:
      while True:
        pass

    # open microcode-maker menu
    if user_choice == 2:
      while True:
        pass
      pass

    # boot the computer
    if user_choice == 3:
      while True:
        pass
      pass

    # invalid option
    else:
      os.system('cls' if os.name == 'nt' else 'clear')    # just clear screen
      print("\033[31m!! Invalid option, try again. (availible option (1, 2 or 3)\033[m")

if __name__ == "__main__":
  main()