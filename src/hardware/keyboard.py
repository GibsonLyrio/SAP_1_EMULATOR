import keyboard as kb

def keyboard_process(input_queue, output_queue):
  listenning = True
  while True:

    # Captura uma tecla pressionada
    key = kb.read_event()

    # keyboard listen all inputs
    if (key.event_type == kb.KEY_DOWN) and (listenning == True):

      # <F1> key #
      if key.name=="f1":
        listenning = False
        print(f"\033[33m{key.scan_code}\033[m")
        print(f"\033[31mPAUSE LISNTEN\033[m")

      # default case #
      else:
        print(f"\033[35mTecla pressionada: {key.scan_code}\033[m")
        output_queue.put(key.scan_code)

    # keyboard don`t listen input, only wait for <F2> key to return listen
    elif (key.event_type == kb.KEY_DOWN) and (key.name == "f2"):
      print(f"\033[32mRESUME LISNTEN\033[m")
      listenning = True