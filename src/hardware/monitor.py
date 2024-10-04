def monitor_process(input_queue):
  while True:
    # Recebe o valor da tecla e imprime no monitor
    key = input_queue.get()
    print(f"Monitor recebeu: {key}")